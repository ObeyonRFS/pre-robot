import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import shutil

PROTO_VERSION = "24.5"  # Change to latest version if needed

def install_python_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

# ------------------ Windows ------------------ #
def install_protoc_windows(version=PROTO_VERSION):
    url = f"https://github.com/protocolbuffers/protobuf/releases/download/v{version}/protoc-{version}-win64.zip"
    print(f"Downloading protoc {version} for Windows...")
    zip_path = "protoc.zip"
    urllib.request.urlretrieve(url, zip_path)
    
    extract_path = os.path.join(os.getcwd(), "protoc")
    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    bin_path = os.path.join(extract_path, "bin")
    
    # Permanently add to user PATH

    # subprocess.run(f'setx PATH "%PATH%;{bin_path}"', shell=True)
    subprocess.run(f'setx PATH "{os.environ["PATH"]};{bin_path}"', shell=True)
    
    print(f"protoc installed at {bin_path} and added to PATH globally (user-level).")
    os.remove(zip_path)

# ------------------ Linux/Ubuntu ------------------ #
def install_protoc_ubuntu(version=PROTO_VERSION):
    try:
        print("Installing protobuf compiler using apt...")
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "install", "-y", "protobuf-compiler"])
        print("protoc installed via apt.")
    except subprocess.CalledProcessError:
        # fallback manual install
        url = f"https://github.com/protocolbuffers/protobuf/releases/download/v{version}/protoc-{version}-linux-x86_64.zip"
        print(f"Downloading protoc {version} for Linux...")
        zip_path = "protoc.zip"
        urllib.request.urlretrieve(url, zip_path)
        extract_path = os.path.join(os.getcwd(), "protoc")
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        bin_path = os.path.join(extract_path, "bin")
        
        # Permanently add to ~/.bashrc
        bashrc_path = os.path.expanduser("~/.bashrc")
        path_line = f'\nexport PATH="{bin_path}:$PATH"\n'
        with open(bashrc_path, "a") as f:
            f.write(path_line)
        print(f"protoc installed at {bin_path} and added to PATH via ~/.bashrc.")
        os.remove(zip_path)

# ------------------ Main ------------------ #
def main():
    print(f"Detected OS: {platform.system()}")
    print("Installing Python protobuf library...")
    install_python_package("protobuf")
    
    if platform.system() == "Windows":
        install_protoc_windows()
    elif platform.system() == "Linux":
        install_protoc_ubuntu()
    else:
        print("Unsupported OS. Please install protoc manually.")
    
    try:
        subprocess.check_call(["protoc", "--version"])
        print("Protobuf installation successful!")
        print("For Windows, please restart your machine before proceeding further.")
    except FileNotFoundError:
        print("Could not verify protoc installation. You may need to restart your terminal.")

if __name__ == "__main__":
    main()
