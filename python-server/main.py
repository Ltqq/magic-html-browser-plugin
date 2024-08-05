from flask import Flask, request, jsonify, send_file
from magic_html import GeneralExtractor
from flask_cors import CORS
import requests
import markdownify
import os
import logging

app = Flask(__name__)

# 启用 CORS，允许所有域的请求（注意：在生产环境中应限制允许的域）
CORS(app, resources={r"/convert": {"origins": "*"}})

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    if 'url' not in data:
        app.logger.error('No URL provided')
        return jsonify({'error': 'No URL provided'}), 400

    url = data['url']
    app.logger.info(f'Received URL: {url}')

    try:
        # 获取HTML内容
        response = requests.get(url, verify=False)
        response.raise_for_status()
        html_content = response.text
        app.logger.info('Fetched HTML content successfully')

        extractor = GeneralExtractor()
        extracted_data = extractor.extract(html_content, base_url=url)
        app.logger.info('Extracted data successfully')

        html_data = extracted_data['html']
        app.logger.info('Extracted HTML data')

        # 使用markdownify将HTML转换为Markdown
        markdown_content = markdownify.markdownify(html_data, heading_style="ATX")
        app.logger.info('Converted HTML to Markdown successfully')

        # 将Markdown内容写入文件
        markdown_file_path = 'output.md'
        with open(markdown_file_path, 'w') as markdown_file:
            markdown_file.write(markdown_content)
        app.logger.info('Markdown content written to file successfully')

        # 提供文件下载并删除文件
        response = send_file(markdown_file_path, as_attachment=True, download_name='output.md')
        response.call_on_close(lambda: os.remove(markdown_file_path))
        app.logger.info('File sent and scheduled for deletion')

        return response

    except requests.exceptions.RequestException as e:
        app.logger.error(f'RequestException: {str(e)}')
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        app.logger.error(f'Exception: {str(e)}')
        return jsonify({'error': 'An error occurred during conversion'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
