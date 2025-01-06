import os
import yaml
import argparse
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class AnsibleDocGenerator:
    def __init__(self, role_directory: str, output_path: Optional[str] = None, logging_directory: str = "logs"):
        """
        Initialize the Ansible documentation generator.
        
        Args:
            role_directory (str): Path to the Ansible role directory
            output_path (Optional[str]): Path where documentation will be saved
            logging_directory (str): Directory for log files
        """
        self.role_directory = role_directory
        self.output_path = output_path or os.path.join(role_directory, 'DOCUMENTATION.md')
        self.logger = self._setup_logging(logging_directory)

    def _setup_logging(self, logging_directory: str) -> logging.Logger:
        """Configure enhanced logging system with rotation"""
        Path(logging_directory).mkdir(exist_ok=True)
        log_file = os.path.join(logging_directory, f"docgen_{datetime.now():%Y%m%d_%H%M%S}.log")
        
        logger = logging.getLogger("AnsibleDocGenerator")
        logger.setLevel(logging.INFO)
        
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger

    def _read_yaml_file(self, file_path: str) -> Dict:
        """
        Read and parse YAML files with enhanced error handling.
        
        Args:
            file_path (str): Path to the YAML file
            
        Returns:
            Dict: Parsed YAML content or empty dict if file doesn't exist
        """
        if not os.path.exists(file_path):
            self.logger.warning(f"File not found: {file_path}")
            return {}
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            self.logger.error(f"YAML parsing error in {file_path}: {str(e)}")
            return {}
        except Exception as e:
            self.logger.error(f"Error reading {file_path}: {str(e)}")
            return {}

    def _validate_role_structure(self) -> Dict[str, bool]:
        """
        Validate Ansible role structure with detailed feedback.
        
        Returns:
            Dict[str, bool]: Dictionary indicating presence of each directory
        """
        required_dirs = ['meta', 'tasks', 'defaults', 'handlers', 'vars', 'templates', 'files']
        structure = {}
        
        for dir_name in required_dirs:
            dir_path = os.path.join(self.role_directory, dir_name)
            exists = os.path.isdir(dir_path)
            structure[dir_name] = exists
            
            if not exists:
                self.logger.warning(f"Missing directory: {dir_name}")
            
        return structure

    def _get_role_variables(self) -> Dict[str, Any]:
        """
        Extract and combine variables from defaults and vars.
        
        Returns:
            Dict[str, Any]: Combined variables from defaults and vars
        """
        defaults = self._read_yaml_file(os.path.join(self.role_directory, 'defaults', 'main.yml'))
        vars_data = self._read_yaml_file(os.path.join(self.role_directory, 'vars', 'main.yml'))
        
        return {
            'defaults': defaults,
            'vars': vars_data
        }

    def _get_tasks_info(self) -> List[Dict[str, str]]:
        """
        Extract information about tasks from main.yml and included files.
        
        Returns:
            List[Dict[str, str]]: List of task information
        """
        tasks_dir = os.path.join(self.role_directory, 'tasks')
        tasks_info = []
        
        if not os.path.exists(tasks_dir):
            return tasks_info
            
        for root, _, files in os.walk(tasks_dir):
            for file in files:
                if file.endswith(('.yml', '.yaml')):
                    file_path = os.path.join(root, file)
                    tasks = self._read_yaml_file(file_path)
                    
                    if isinstance(tasks, list):
                        for task in tasks:
                            if isinstance(task, dict) and 'name' in task:
                                # Processa as tags de forma adequada
                                tags = task.get('tags', [])
                                # Se tags for uma string, converte para lista
                                if isinstance(tags, str):
                                    tags = [tags]
                                # Se for lista, junta com vírgulas
                                tags_str = ', '.join(tags) if tags else ''
                                
                                tasks_info.append({
                                    'name': task['name'],
                                    'file': os.path.relpath(file_path, tasks_dir),
                                    'tags': tags_str
                                })
                                
        return tasks_info

    def _format_platforms(self, platforms: List[Dict]) -> str:
        """Format platform information for documentation"""
        if not platforms:
            return "- No platform information specified"
            
        platform_info = []
        for platform in platforms:
            name = platform.get('name', 'Unknown')
            versions = platform.get('versions', ['All'])
            versions_str = ', '.join(str(v) for v in versions if v != 'all')
            platform_info.append(f"- {name}: {versions_str if versions_str else 'All versions'}")
            
        return '\n'.join(platform_info)

    def _format_dependencies(self, dependencies: List) -> str:
        """Format role dependencies for documentation"""
        if not dependencies:
            return "No dependencies specified"
            
        dep_info = []
        for dep in dependencies:
            if isinstance(dep, str):
                dep_info.append(f"- {dep}")
            elif isinstance(dep, dict):
                name = dep.get('role', 'Unknown')
                version = dep.get('version', 'latest')
                dep_info.append(f"- {name} (version: {version})")
                
        return '\n'.join(dep_info)

    def _get_handlers_info(self) -> List[Dict[str, str]]:
        """
        Extract information about handlers.
        
        Returns:
            List[Dict[str, str]]: List of handler information
        """
        handlers_file = os.path.join(self.role_directory, 'handlers', 'main.yml')
        handlers = self._read_yaml_file(handlers_file)
        
        handlers_info = []
        if isinstance(handlers, list):
            for handler in handlers:
                if isinstance(handler, dict) and 'name' in handler:
                    handlers_info.append({
                        'name': handler['name'],
                        'listen': handler.get('listen', '')
                    })
                    
        return handlers_info

    def generate_documentation(self) -> str:
        """
        Generate comprehensive role documentation.
        
        Returns:
            str: Generated documentation in Markdown format
        """
        self.logger.info("Starting documentation generation")
        
        structure = self._validate_role_structure()
        
        meta = self._read_yaml_file(os.path.join(self.role_directory, 'meta', 'main.yml'))
        galaxy_info = meta.get('galaxy_info', {})
        
        variables = self._get_role_variables()
        tasks = self._get_tasks_info()
        handlers = self._get_handlers_info()
        
        # Gera o conteúdo da documentação
        role_name = galaxy_info.get('role_name', 'Ansible Role')
        description = galaxy_info.get('description', 'No description provided')
        author = galaxy_info.get('author', 'Unknown')
        license = galaxy_info.get('license', 'Unknown')
        min_ansible_version = galaxy_info.get('min_ansible_version', 'Not specified')
        
        # Controi a estrutura do diretório
        dir_structure = ''
        for dir_name, exists in structure.items():
            check_mark = '✓' if exists else '✗'
            dir_structure += f"- {dir_name}/: {check_mark}\n"

        tasks_section = ''
        for task in tasks:
            task_name = task['name']
            task_file = task['file']
            task_tags = task['tags']
            tasks_section += f"- {task_name} ({task_file})"
            if task_tags:
                tasks_section += f" [Tags: {task_tags}]"
            tasks_section += "\n"
        # Controi a seção de handlers
        handlers_section = ''
        for handler in handlers:
            handler_name = handler['name']
            handler_listen = handler['listen']
            handlers_section += f"- {handler_name}"
            if handler_listen:
                handlers_section += f" (listen: {handler_listen})"
            handlers_section += "\n"

        doc_content = f"""# {role_name}

## Description
{description}

## Role Information
- **Author:** {author}
- **License:** {license}
- **Minimum Ansible Version:** {min_ansible_version}

## Directory Structure
{dir_structure}

## Supported Platforms
{self._format_platforms(galaxy_info.get('platforms', []))}

## Role Dependencies
{self._format_dependencies(meta.get('dependencies', []))}

## Role Variables

### Defaults
```yaml
{yaml.dump(variables['defaults'], default_flow_style=False, sort_keys=False)}
```

### Variables
```yaml
{yaml.dump(variables['vars'], default_flow_style=False, sort_keys=False)}
```

## Tasks
{tasks_section}

## Handlers
{handlers_section}

## Example Playbook
```yaml
- hosts: servers
  roles:
    - role: {role_name}
```

## License
This role is licensed under {license}.

## Author Information
Created by {author}

---
*Documentation generated on {datetime.now():%Y-%m-%d %H:%M:%S}*
"""
        
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(doc_content)
            self.logger.info(f"Documentation saved to {self.output_path}")
        except Exception as e:
            self.logger.error(f"Error saving documentation: {str(e)}")
            
        return doc_content
    
def initialize_argument_parser() -> argparse.ArgumentParser:
    """
    Initialize and configure the argument parser with detailed help messages.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="""
        Ansible Role Documentation Generator

        This tool automatically generates comprehensive documentation for Ansible roles.
        It analyzes the role structure and creates a detailed Markdown document including:
        - Role metadata and description
        - Directory structure validation
        - Variables from defaults and vars
        - Tasks and handlers information
        - Platform support and dependencies
        - Example playbook usage
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'role_directory',
        help='Path to the Ansible role directory to analyze'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output path for the generated documentation (default: DOCUMENTATION.md in role directory)',
        metavar='PATH'
    )

    parser.add_argument(
        '--logs', '-l',
        default='logs',
        help='Directory for storing log files (default: ./logs)',
        metavar='DIR'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=0,
        help='Increase verbosity level (can be used multiple times)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0',
        help='Show program version number and exit'
    )

    return parser

def main():
    parser = initialize_argument_parser()
    args = parser.parse_args()
    
    try:
        doc_generator = AnsibleDocGenerator(
            role_directory=args.role_directory,
            output_path=args.output,
            logging_directory=args.logs
        )
        doc_generator.generate_documentation()
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == '__main__':
    exit(main())