import argparse
import dataclasses
import os
import subprocess
import threading

import docker


class UpdateType:
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"

    @classmethod
    def from_str(cls, update_type: str):
        if update_type == cls.MAJOR:
            return cls.MAJOR
        elif update_type == cls.MINOR:
            return cls.MINOR
        elif update_type == cls.PATCH:
            return cls.PATCH
        else:
            raise ValueError(f"Invalid update type: {update_type}")


@dataclasses.dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def from_str(cls, version: str):
        major, minor, patch = map(int, version.split("."))
        return cls(major, minor, patch)

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other):
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __eq__(self, other):
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __gt__(self, other):
        return (self.major, self.minor, self.patch) > (other.major, other.minor, other.patch)

    def update_major(self):
        return Version(self.major + 1, 0, 0)

    def update_minor(self):
        return Version(self.major, self.minor + 1, 0)

    def update_patch(self):
        return Version(self.major, self.minor, self.patch + 1)

    def update(self, update_type: UpdateType):
        if update_type == UpdateType.MAJOR:
            return self.update_major()
        elif update_type == UpdateType.MINOR:
            return self.update_minor()
        elif update_type == UpdateType.PATCH:
            return self.update_patch()
        else:
            raise ValueError(f"Invalid update type: {update_type}")

    def get_docker_image_name(self):
        return f"softotobo/atc-basic:{str(self)}"


def execute_command(command: str):
    def print_output(stream):
        while True:
            output = stream.readline()
            if output:
                print(output.strip())
            else:
                break

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True,
                               bufsize=1)

    stdout_thread = threading.Thread(target=print_output, args=(process.stdout,))
    stdout_thread.start()

    stderr_thread = threading.Thread(target=print_output, args=(process.stderr,))
    stderr_thread.start()

    process.wait()

    stdout_thread.join()
    stderr_thread.join()


def get_current_version() -> Version:
    with open("../../dataset-generator/data/versions") as file:
        return Version.from_str(file.read().split("\n")[0].strip())


def build_new_image(update_type: UpdateType = UpdateType.PATCH):
    current_version = get_current_version()
    next_version = current_version.update(update_type)
    client = docker.from_env()
    username = os.getenv('DOCKER_USERNAME')
    password = os.getenv('DOCKER_PASSWORD')
    client.login(username=username, password=password)
    image_name = next_version.get_docker_image_name()

    print(f"Building Docker image: {image_name}...")
    _, build_logs = client.images.build(path="..", tag=image_name)
    for log in build_logs:
        print(log.get('stream', '').strip())

    print("Logging in to DockerHub...")

    print(f"Pushing image to DockerHub: {image_name}...")
    push_logs = client.images.push(image_name, stream=True)
    for log in push_logs:
        print(log)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Build and push Docker image to DockerHub.")
    parser.add_argument("--update-type", help="Update Type: major, minor, or patch. Default is patch.",
                        default=str(UpdateType.PATCH), nargs="?")
    args = parser.parse_args()
    build_new_image(UpdateType.from_str(args.update_type))
