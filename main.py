from bestconfig import Config
from core.parsers.article_parsers import ScientificamericanParser

def main():
    config = Config()
    print(config['version'])
    parser = ScientificamericanParser()
    
    

if __name__ == '__main__':
    main()