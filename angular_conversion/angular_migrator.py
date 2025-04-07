import os
import json
from dotenv import load_dotenv
import argparse
import fnmatch
import time
import anthropic


load_dotenv(override=True)
os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY', '')


claude = anthropic.Anthropic()
CLAUDE_MODEL = "claude-3-7-sonnet-latest"


def should_ignore_file(file_path):
    """Checks if the file should be ignored during migration."""
    ignore_patterns = ["package.json","README.md","/src/browserslist","/src/index.html","/src/favicon.ico","/src/karma.conf.js","/src/test.ts","angular.json","tsconfig.json","tslint.json","*.spec.ts", "/src/assets/*",".settings/*","node_modules/*","e2e/*", ".gitignore", ".angular", ".vscode", ".idea", "dist/*", ".project","/src/environments/*","/src/browserslist","/src/favicon.ico","karma.conf.js","LICENSE",".editorconfig"]
    return any(fnmatch.fnmatch(file_path, pattern) for pattern in ignore_patterns)

def get_project_dependencies(source_path):
    """Extracts Angular project dependencies from package.json."""
    package_json_path = os.path.join(source_path, "package.json")
    if not os.path.exists(package_json_path):
        print("package.json not found in source path!")
        return None
    
    with open(package_json_path, "r") as file:
        package_data = json.load(file)
    
    return package_data

def detect_current_angular_version(dependencies):
    """Detects the current Angular version from package.json dependencies."""
    angular_core_version = dependencies.get("@angular/core", "")
    return angular_core_version.lstrip("^").split(".")[0] if angular_core_version else "unknown"

def fetch_recommended_dependencies(dependencies,target_version):
    """Fetch recommended dependencies dynamically using Claude AI."""
    package_list = ", ".join([f"{pkg}@{ver}" for pkg, ver in dependencies.items()])

    prompt = (
        f"Given the following npm packages and their versions:\n\n"
        f"{package_list}\n\n"
        f"Upgrade these dependencies to be compatible with Angular {target_version}. "
        f"Provide the best recommended versions for all of them in a valid JSON format."
    )

    system_message = "You are an expert Angular developer and expert in npm dependencies. Respond only with code without any explaination. "

    userMessage = [{"role": "user", "content": prompt}]

    print(f"Prompt to Claude AI : {userMessage}")
    try:
        response = claude.messages.stream(
            model=CLAUDE_MODEL,
            max_tokens=64000,
            system=system_message,
            messages=userMessage
        )

        reply = ""
        with response as stream:
            for text in stream.text_stream:
             reply += text
        reply = reply.replace('```json','').replace('```','')
        print(f"Response from Claude AI : {reply}")
        recommended_versions  = json.loads(reply)
        return recommended_versions
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error fetching recommended dependencies: {e}")
        return dependencies  # Fallback to current versions


def update_json_file(source_path, destination_path, filename, modifications):
    """Reads a JSON file, applies modifications, and writes to destination."""
    source_file = os.path.join(source_path, filename)
    dest_file = os.path.join(destination_path, filename)
    
    if not os.path.exists(source_file):
        return
    
    with open(source_file, "r") as file:
        data = json.load(file)
    
    data.update(modifications)
    
    os.makedirs(destination_path, exist_ok=True)
    with open(dest_file, "w") as file:
        json.dump(data, file, indent=2)
    
    print(f"Updated {filename} saved to {dest_file}")

def update_package_json(source_path, destination_path, target_version):
    """Updates package.json with the target Angular version and other dependencies."""
    package_data = get_project_dependencies(source_path)
    if package_data is None:
        return
    
    dependencies = package_data.get("dependencies", {})
    dev_dependencies = package_data.get("devDependencies", {})
    current_version = detect_current_angular_version(dependencies)
    
    print(f"Detected current Angular version: {current_version}")
    print(f"Upgrading to Angular version: {target_version}")
    print(f"Fetching recommended versions for Angular {target_version}...")

    recommended_dependencies = fetch_recommended_dependencies(dependencies, target_version)
    recommended_dev_dependencies = fetch_recommended_dependencies(dev_dependencies, target_version)
    package_data["dependencies"] = recommended_dependencies
    package_data["devDependencies"] = recommended_dev_dependencies
    
    dest_package_json_path = os.path.join(destination_path, "package.json")
    os.makedirs(destination_path, exist_ok=True)

    with open(dest_package_json_path, "w", encoding="utf-8", errors='ignore') as file:
        json.dump(package_data, file, indent=2)

    print(f"Updated package.json saved to {dest_package_json_path}")

def analyze_code_for_migration(source_path, destination_path, current_version, target_version):
    """Uses ClaudeAI API to analyze project files and suggest migrations."""
    
    for root, _, files in os.walk(source_path):
        for file_name in files:
            rel_path = os.path.relpath(os.path.join(root, file_name), source_path)
            source_file_path = os.path.join(root, file_name)
            dest_file_path = os.path.join(destination_path, rel_path)

            if should_ignore_file(rel_path):
                print(f"Skipping {rel_path} (ignored)")
              #  if os.path.exists(source_file_path):
              #      with open(source_file_path, "r", encoding="utf-8") as file:
              #          code_content = file.read()
              #  os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
              #  with open(dest_file_path, "w", encoding="utf-8") as file:
              #      file.write(code_content)
              #  print(f"Updated {dest_file_path} without calling claude AI")
                continue  # Skip ignored files
            


            if os.path.exists(source_file_path):
                with open(source_file_path, "r", encoding="utf-8", errors='ignore') as file:
                    code_content = file.read()
                
            prompt = (
                f"Upgrade this Angular {rel_path} file from version {current_version} to {target_version} "
                f"while keeping it minimal and readable. If you are upgrading to version 16 or above then use standalone components instead of module structure:\n{code_content}"
            )

            print(f"Calling claude to Upgrade this Angular {rel_path} file from version {current_version} to {target_version}")

            userMessage = [{"role": "user", "content": prompt}]
            system_message = "You are an expert Angular developer.Respond only with code without any explaination"

            response = claude.messages.stream(
                model=CLAUDE_MODEL,
                max_tokens=64000,
                system=system_message,
                messages=userMessage
            )
            
            suggested_code = ""
            with response as stream:
                for text in stream.text_stream:
                    suggested_code += text
            suggested_code = suggested_code.replace('```typescript','')
            suggested_code = suggested_code.replace('```css','')
            suggested_code = suggested_code.replace('```html','')
            suggested_code = suggested_code.replace('```json','')
            suggested_code = suggested_code.replace('```javascript','')
            suggested_code = suggested_code.replace('```','')
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
            with open(dest_file_path, "w", encoding="utf-8", errors='ignore') as file:
                file.write(suggested_code)
            
            print(f"Updated {dest_file_path}")

def run_migration_tool(source_path, destination_path, target_version):
    """Main function to run the Angular upgrade tool."""
    print("Starting Angular upgrade tool...")
    package_data = get_project_dependencies(source_path)
    if package_data is None:
        return
    
    dependencies = package_data.get("dependencies", {})
    current_version = detect_current_angular_version(dependencies)
    
    update_package_json(source_path, destination_path, target_version)
    update_json_file(source_path, destination_path, "angular.json", {})
    update_json_file(source_path, destination_path, "tsconfig.json", {})
    update_json_file(source_path, destination_path, "tslint.json", {})
    
    analyze_code_for_migration(source_path, destination_path, current_version, target_version)
    print("Angular upgrade complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Angular Upgrade Tool")
    parser.add_argument("source_path", type=str, help="Path to the source Angular project")
    parser.add_argument("destination_path", type=str, help="Path to save the upgraded Angular project")
    parser.add_argument("target_version", type=str, help="Target Angular version")
    args = parser.parse_args()
    
    run_migration_tool(args.source_path, args.destination_path, args.target_version)
