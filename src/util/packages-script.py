import os
import sys


def get_package_sizes():
    # Get the location of the site-packages directory within the active virtual environment
    site_packages = next(p for p in sys.path if 'site-packages' in p and '.venv' in p)

    installed_packages = os.listdir(site_packages)

    package_sizes = []
    for package in installed_packages:
        package_path = os.path.join(site_packages, package)
        total_size = 0

        for dirpath, dirnames, filenames in os.walk(package_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        total_size_mb = total_size / (1024 * 1024)
        package_sizes.append((package, total_size_mb))

    return package_sizes


def main():
    package_sizes = get_package_sizes()

    sorted_packages = sorted(package_sizes, key=lambda x: x[1], reverse=True)

    print("Top 10 largest installed packages in the virtual environment:")
    for package, size in sorted_packages[:10]:
        print(f"{package}: {size:.2f} MB")


if __name__ == '__main__':
    main()
