import os
import re

dir_path = r"d:\savannakhet-project\frontend\src"

def replace_api(content):
    c = content
    c = re.sub(r"api\.get\(['`]/places['`]\)", "placeRepository.getAll()", c)
    c = re.sub(r"api\.get\(['`]/places\?include_drafts=true['`]\)", "placeRepository.getAll(true)", c)
    c = re.sub(r"api\.get\(['`]/categories['`]\)", "categoryRepository.getAll()", c)
    c = re.sub(r"api\.get\(`\/places\/\$\{([a-zA-Z0-9_\.]+)\}`\)", r"placeRepository.getById(\1)", c)
    c = re.sub(r"api\.post\(['`]/places['`], ([^\n\)]+)\)", r"placeRepository.create(\1)", c)
    
    # Note: Vue API calls might have trailing stuff, so regex needs to be careful
    c = re.sub(r"api\.put\(`\/places\/\$\{([a-zA-Z0-9_\.]+)\}`, ([^\n\)]+)\)", r"placeRepository.update(\1, \2)", c)
    c = re.sub(r"api\.put\(`\/admin\/places\/\$\{([a-zA-Z0-9_\.]+)\}`, ([^\n\)]+)\)", r"placeRepository.update(\1, \2)", c)
    c = re.sub(r"api\.delete\(`\/admin\/places\/\$\{([a-zA-Z0-9_\.]+)\}`\)", r"placeRepository.delete(\1)", c)
    c = re.sub(r"api\.delete\(`\/places\/\$\{([a-zA-Z0-9_\.]+)\}`\)", r"placeRepository.delete(\1)", c)
    
    c = re.sub(r"api\.get\(`\/places\/\$\{([a-zA-Z0-9_\.]+)\}\/comments`\)", r"placeRepository.getComments(\1)", c)
    c = re.sub(r"api\.post\(`\/places\/\$\{([a-zA-Z0-9_\.]+)\}\/comments`, ([^\n\)]+)\)", r"placeRepository.addComment(\1, \2)", c)
    c = re.sub(r"api\.get\(['`]\/admin\/all-comments['`]\)", r"placeRepository.getAllComments()", c)
    c = re.sub(r"api\.delete\(`\/comments\/\$\{([a-zA-Z0-9_\.]+)\}`\)", r"placeRepository.deleteComment(\1)", c)
    
    c = re.sub(r"api\.post\(['`]\/categories['`], ([^\n\)]+)\)", r"categoryRepository.create(\1)", c)
    c = re.sub(r"api\.delete\(`\/categories\/\$\{([a-zA-Z0-9_\.]+)\}`\)", r"categoryRepository.delete(\1)", c)
    
    c = re.sub(r"api\.get\(['`]\/users['`]\)", r"userRepository.getAll()", c)
    c = re.sub(r"api\.put\(`\/users\/\$\{([a-zA-Z0-9_\.]+)\}`, ([^\n\)]+)\)", r"userRepository.update(\1, \2)", c)
    c = re.sub(r"api\.patch\(`\/users\/\$\{([a-zA-Z0-9_\.]+)\}\/soft-delete`\)", r"userRepository.softDelete(\1)", c)
    c = re.sub(r"api\.patch\(`\/users\/\$\{([a-zA-Z0-9_\.]+)\}\/restore`\)", r"userRepository.restore(\1)", c)
    return c

for root, _, files in os.walk(dir_path):
    for fl in files:
        if fl.endswith('.vue') and fl not in ['Login.vue', 'Register.vue']:
            filepath = os.path.join(root, fl)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            old = content
            content = replace_api(content)
            
            if content != old:
                repos_used = []
                if "placeRepository." in content: repos_used.append("placeRepository")
                if "categoryRepository." in content: repos_used.append("categoryRepository")
                if "userRepository." in content: repos_used.append("userRepository")
                if "authRepository." in content: repos_used.append("authRepository")
                
                new_imports = ""
                for repo in repos_used:
                    new_imports += f"import {{ {repo} }} from '@/repositories/{repo}'\n"
                    
                content = content.replace("import api from '@/services/api'", new_imports.strip())
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {fl}")
