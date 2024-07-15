def main():
    import subprocess

    excluded_packages = {'torch', 'torchvision', 'torchaudio'}

    with open('../base-requirements.txt') as file:
        base_requirements = set(line.strip() for line in file if line.strip())

    pip_freeze_output = subprocess.check_output(['pip', 'freeze']).decode()
    current_requirements = set(pip_freeze_output.strip().split('\n'))

    current_requirements = {req for req in current_requirements if req.split('==')[0] not in excluded_packages}

    new_requirements = current_requirements - base_requirements

    with open('../requirements.txt', 'w') as file:
        for requirement in sorted(new_requirements):
            file.write(requirement)


if __name__ == '__main__':
    main()
