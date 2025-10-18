import os
import requests
from urllib.parse import urlparse


URL = os.getenv('CLASH_DOMAINS_URL')
OUTPUT_DIR = 'ConvertedRules'

def generate_and_save_rules():
    """
    从 URL 下载规则，根据 URL 的文件名自动命名输出文件，并保存到指定目录。
    """
    if not URL:
        print("错误: 环境变量 'CLASH_DOMAINS_URL' 未设置。")
        exit(1)


    try:
        path = urlparse(URL).path
        filename = os.path.basename(path)

        if not filename:
            print(f"错误: 无法从 URL 中提取有效的文件名: {URL}")
            exit(1)
        
        # 将输出目录和自动获取的文件名组合成最终路径
        # 例如: 'rules' + 'Global.list' -> 'rules/Global.list'
        output_file_path = os.path.join(OUTPUT_DIR, filename)

    except Exception as e:
        print(f"解析 URL 或生成文件路径时出错: {e}")
        exit(1)


    if not os.path.exists(OUTPUT_DIR):
        print(f"目录 '{OUTPUT_DIR}' 不存在，正在创建...")
        os.makedirs(OUTPUT_DIR)

    print(f"正在从 URL 下载规则: {URL}")
    try:
        response = requests.get(URL, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        lines = response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"错误: 下载规则失败。原因: {e}")
        exit(1)

    all_rules = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('+.'):
            all_rules.append(f"DOMAIN-SUFFIX,{line[2:]}")
        else:
            all_rules.append(f"DOMAIN,{line}")
    
    print(f"处理完成。共生成 {len(all_rules)} 条规则。")
    all_rules.sort()

    print(f"正在写入所有规则到: {output_file_path}")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_rules))
        f.write('\n')

    print("所有任务已完成！")

if __name__ == '__main__':
    generate_and_save_rules()
