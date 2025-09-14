"""
Vollständiger Test aller 63 MCP Docassemble Endpunkte
Testet jeden einzelnen Endpunkt und markiert Status
"""

import sys
import os
sys.path.insert(0, 'src')

from mcp_docassemble.client import DocassembleClient
from dotenv import load_dotenv
import json

def test_all_endpoints():
    print("🧪 VOLLSTÄNDIGER ENDPUNKT-TEST")
    print("="*60)
    
    # Lade Umgebungsvariablen
    load_dotenv()
    
    # Erstelle Enhanced Client
    client = DocassembleClient(
        base_url=os.getenv('DOCASSEMBLE_BASE_URL', 'http://192.168.178.29:8080'),
        api_key=os.getenv('DOCASSEMBLE_API_KEY', '5DHxBg6f1vchBcnKCmSIDxhc6REorsHp'),
        timeout=30,
        session_timeout=7200,
        enable_fallbacks=True
    )
    
    results = {
        'working': [],
        'not_working': [],
        'partial': [],
        'total_tested': 0
    }
    
    # Test-Session für Session-basierte Endpunkte
    test_session = None
    try:
        session_result = client.start_interview('docassemble.demo:data/questions/questions.yml')
        if session_result and 'session' in session_result:
            test_session = session_result['session']
            print(f"✅ Test-Session erstellt: {test_session[:20]}...")
    except Exception as e:
        print(f"⚠️ Keine Test-Session verfügbar: {e}")
    
    print(f"\n📊 TESTE ALLE ENDPUNKTE...")
    print("-" * 60)
    
    # 1. USER MANAGEMENT ENDPOINTS
    print(f"\n👥 USER MANAGEMENT (9 Endpunkte)")
    
    # get_user_info
    try:
        result = client.get_user_info()
        results['working'].append('get_user_info')
        print(f"   ✅ get_user_info")
    except Exception as e:
        results['not_working'].append(('get_user_info', str(e)[:100]))
        print(f"   ❌ get_user_info: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # list_users  
    try:
        result = client.list_users()
        results['working'].append('list_users')
        print(f"   ✅ list_users")
    except Exception as e:
        results['not_working'].append(('list_users', str(e)[:100]))
        print(f"   ❌ list_users: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # create_user
    try:
        result = client.create_user('test@example.com', 'TestPassword123!')
        results['working'].append('create_user')
        print(f"   ✅ create_user")
    except Exception as e:
        results['not_working'].append(('create_user', str(e)[:100]))
        print(f"   ❌ create_user: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # delete_user_account
    try:
        result = client.delete_user_account('test@example.com')
        results['working'].append('delete_user_account')
        print(f"   ✅ delete_user_account")
    except Exception as e:
        results['not_working'].append(('delete_user_account', str(e)[:100]))
        print(f"   ❌ delete_user_account: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # set_user_info
    try:
        result = client.set_user_info(email='test@example.com', first_name='Test')
        results['working'].append('set_user_info')
        print(f"   ✅ set_user_info")
    except Exception as e:
        results['not_working'].append(('set_user_info', str(e)[:100]))
        print(f"   ❌ set_user_info: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # get_user_privileges
    try:
        result = client.get_user_privileges('test@example.com')
        results['working'].append('get_user_privileges')
        print(f"   ✅ get_user_privileges")
    except Exception as e:
        results['not_working'].append(('get_user_privileges', str(e)[:100]))
        print(f"   ❌ get_user_privileges: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # set_user_privileges
    try:
        result = client.set_user_privileges('test@example.com', ['user'])
        results['working'].append('set_user_privileges')
        print(f"   ✅ set_user_privileges")
    except Exception as e:
        results['not_working'].append(('set_user_privileges', str(e)[:100]))
        print(f"   ❌ set_user_privileges: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # reset_user_password
    try:
        result = client.reset_user_password('test@example.com')
        results['working'].append('reset_user_password')
        print(f"   ✅ reset_user_password")
    except Exception as e:
        results['not_working'].append(('reset_user_password', str(e)[:100]))
        print(f"   ❌ reset_user_password: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # change_user_password
    try:
        result = client.change_user_password('old_pass', 'new_pass')
        results['working'].append('change_user_password')
        print(f"   ✅ change_user_password")
    except Exception as e:
        results['not_working'].append(('change_user_password', str(e)[:100]))
        print(f"   ❌ change_user_password: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # 2. INTERVIEW MANAGEMENT ENDPOINTS  
    print(f"\n📝 INTERVIEW MANAGEMENT (12 Endpunkte)")
    
    # start_interview
    try:
        result = client.start_interview('docassemble.demo:data/questions/questions.yml')
        results['working'].append('start_interview')
        print(f"   ✅ start_interview")
    except Exception as e:
        results['not_working'].append(('start_interview', str(e)[:100]))
        print(f"   ❌ start_interview: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # get_interview_variables
    if test_session:
        try:
            result = client.get_interview_variables(test_session, 'docassemble.demo:data/questions/questions.yml')
            results['working'].append('get_interview_variables')
            print(f"   ✅ get_interview_variables")
        except Exception as e:
            results['not_working'].append(('get_interview_variables', str(e)[:100]))
            print(f"   ❌ get_interview_variables: {str(e)[:50]}...")
    else:
        results['not_working'].append(('get_interview_variables', 'No test session available'))
        print(f"   ❌ get_interview_variables: No test session")
    results['total_tested'] += 1
    
    # set_interview_variables
    if test_session:
        try:
            result = client.set_interview_variables(test_session, 'docassemble.demo:data/questions/questions.yml', {'test_var': 'test_value'})
            results['working'].append('set_interview_variables')
            print(f"   ✅ set_interview_variables")
        except Exception as e:
            results['not_working'].append(('set_interview_variables', str(e)[:100]))
            print(f"   ❌ set_interview_variables: {str(e)[:50]}...")
    else:
        results['not_working'].append(('set_interview_variables', 'No test session available'))
        print(f"   ❌ set_interview_variables: No test session")
    results['total_tested'] += 1
    
    # run_interview_action
    if test_session:
        try:
            result = client.run_interview_action(test_session, 'docassemble.demo:data/questions/questions.yml', 'continue')
            results['working'].append('run_interview_action')
            print(f"   ✅ run_interview_action")
        except Exception as e:
            results['not_working'].append(('run_interview_action', str(e)[:100]))
            print(f"   ❌ run_interview_action: {str(e)[:50]}...")
    else:
        results['not_working'].append(('run_interview_action', 'No test session available'))
        print(f"   ❌ run_interview_action: No test session")
    results['total_tested'] += 1
    
    # delete_interview_session
    if test_session:
        try:
            result = client.delete_interview_session(test_session, 'docassemble.demo:data/questions/questions.yml')
            results['working'].append('delete_interview_session')
            print(f"   ✅ delete_interview_session")
        except Exception as e:
            results['not_working'].append(('delete_interview_session', str(e)[:100]))
            print(f"   ❌ delete_interview_session: {str(e)[:50]}...")
    else:
        results['not_working'].append(('delete_interview_session', 'No test session available'))
        print(f"   ❌ delete_interview_session: No test session")
    results['total_tested'] += 1
    
    # list_interview_sessions
    try:
        result = client.list_interview_sessions()
        results['working'].append('list_interview_sessions')
        print(f"   ✅ list_interview_sessions")
    except Exception as e:
        results['not_working'].append(('list_interview_sessions', str(e)[:100]))
        print(f"   ❌ list_interview_sessions: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # list_user_interview_sessions
    try:
        result = client.list_user_interview_sessions()
        results['working'].append('list_user_interview_sessions')
        print(f"   ✅ list_user_interview_sessions")
    except Exception as e:
        results['not_working'].append(('list_user_interview_sessions', str(e)[:100]))
        print(f"   ❌ list_user_interview_sessions: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # list_specific_user_interview_sessions
    try:
        result = client.list_specific_user_interview_sessions('test@example.com')
        results['working'].append('list_specific_user_interview_sessions')
        print(f"   ✅ list_specific_user_interview_sessions")
    except Exception as e:
        results['not_working'].append(('list_specific_user_interview_sessions', str(e)[:100]))
        print(f"   ❌ list_specific_user_interview_sessions: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # list_advertised_interviews
    try:
        result = client.list_advertised_interviews()
        results['working'].append('list_advertised_interviews')
        print(f"   ✅ list_advertised_interviews")
    except Exception as e:
        results['not_working'].append(('list_advertised_interviews', str(e)[:100]))
        print(f"   ❌ list_advertised_interviews: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # get_interview_statistics
    try:
        result = client.get_interview_statistics()
        results['working'].append('get_interview_statistics')
        print(f"   ✅ get_interview_statistics")
    except Exception as e:
        results['not_working'].append(('get_interview_statistics', str(e)[:100]))
        print(f"   ❌ get_interview_statistics: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # restart_interview
    if test_session:
        try:
            result = client.restart_interview(test_session, 'docassemble.demo:data/questions/questions.yml')
            results['working'].append('restart_interview')
            print(f"   ✅ restart_interview")
        except Exception as e:
            results['not_working'].append(('restart_interview', str(e)[:100]))
            print(f"   ❌ restart_interview: {str(e)[:50]}...")
    else:
        results['not_working'].append(('restart_interview', 'No test session available'))
        print(f"   ❌ restart_interview: No test session")
    results['total_tested'] += 1
    
    # rename_interview_session
    if test_session:
        try:
            result = client.rename_interview_session(test_session, 'docassemble.demo:data/questions/questions.yml', 'Test Session')
            results['working'].append('rename_interview_session')
            print(f"   ✅ rename_interview_session")
        except Exception as e:
            results['not_working'].append(('rename_interview_session', str(e)[:100]))
            print(f"   ❌ rename_interview_session: {str(e)[:50]}...")
    else:
        results['not_working'].append(('rename_interview_session', 'No test session available'))
        print(f"   ❌ rename_interview_session: No test session")
    results['total_tested'] += 1
    
    # 3. FILE MANAGEMENT ENDPOINTS
    print(f"\n📁 FILE MANAGEMENT (12 Endpunkte)")
    
    # upload_file
    try:
        test_content = b"Test file content for upload"
        result = client.upload_file(test_content, 'test_upload.txt')
        results['working'].append('upload_file')
        print(f"   ✅ upload_file")
    except Exception as e:
        results['not_working'].append(('upload_file', str(e)[:100]))
        print(f"   ❌ upload_file: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # download_file
    try:
        result = client.download_file(1)  # Test file ID
        results['working'].append('download_file')
        print(f"   ✅ download_file")
    except Exception as e:
        results['not_working'].append(('download_file', str(e)[:100]))
        print(f"   ❌ download_file: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # get_file_info
    try:
        result = client.get_file_info(1)
        results['working'].append('get_file_info')
        print(f"   ✅ get_file_info")
    except Exception as e:
        results['not_working'].append(('get_file_info', str(e)[:100]))
        print(f"   ❌ get_file_info: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # delete_file
    try:
        result = client.delete_file(999)  # Non-existent file
        results['partial'].append('delete_file')
        print(f"   ⚠️ delete_file (partial - test file)")
    except Exception as e:
        results['not_working'].append(('delete_file', str(e)[:100]))
        print(f"   ❌ delete_file: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # list_files
    try:
        result = client.list_files()
        results['working'].append('list_files')
        print(f"   ✅ list_files")
    except Exception as e:
        results['not_working'].append(('list_files', str(e)[:100]))
        print(f"   ❌ list_files: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # convert_file_to_markdown
    try:
        test_content = b"# Test Markdown\nThis is a test."
        result = client.convert_file_to_markdown(test_content, 'test.md')
        results['working'].append('convert_file_to_markdown')
        print(f"   ✅ convert_file_to_markdown")
    except Exception as e:
        results['not_working'].append(('convert_file_to_markdown', str(e)[:100]))
        print(f"   ❌ convert_file_to_markdown: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # convert_file_to_pdf
    try:
        test_content = b"Test content for PDF conversion"
        result = client.convert_file_to_pdf(test_content, 'test.txt')
        results['working'].append('convert_file_to_pdf')
        print(f"   ✅ convert_file_to_pdf")
    except Exception as e:
        results['not_working'].append(('convert_file_to_pdf', str(e)[:100]))
        print(f"   ❌ convert_file_to_pdf: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # create_playground_file
    try:
        result = client.create_playground_file('test.yml', 'Test YAML content')
        results['working'].append('create_playground_file')
        print(f"   ✅ create_playground_file")
    except Exception as e:
        results['not_working'].append(('create_playground_file', str(e)[:100]))
        print(f"   ❌ create_playground_file: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # get_playground_file
    try:
        result = client.get_playground_file('test.yml')
        results['working'].append('get_playground_file')
        print(f"   ✅ get_playground_file")
    except Exception as e:
        results['not_working'].append(('get_playground_file', str(e)[:100]))
        print(f"   ❌ get_playground_file: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # delete_playground_file
    try:
        result = client.delete_playground_file('test.yml')
        results['working'].append('delete_playground_file')
        print(f"   ✅ delete_playground_file")
    except Exception as e:
        results['not_working'].append(('delete_playground_file', str(e)[:100]))
        print(f"   ❌ delete_playground_file: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # list_playground_files
    try:
        result = client.list_playground_files()
        results['working'].append('list_playground_files')
        print(f"   ✅ list_playground_files")
    except Exception as e:
        results['not_working'].append(('list_playground_files', str(e)[:100]))
        print(f"   ❌ list_playground_files: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # list_interview_files
    try:
        result = client.list_interview_files('docassemble.demo')
        results['working'].append('list_interview_files')
        print(f"   ✅ list_interview_files")
    except Exception as e:
        results['not_working'].append(('list_interview_files', str(e)[:100]))
        print(f"   ❌ list_interview_files: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # 4. PACKAGE MANAGEMENT ENDPOINTS
    print(f"\n📦 PACKAGE MANAGEMENT (6 Endpunkte)")
    
    # list_package_management
    try:
        result = client.list_package_management()
        results['working'].append('list_package_management')
        print(f"   ✅ list_package_management")
    except Exception as e:
        results['not_working'].append(('list_package_management', str(e)[:100]))
        print(f"   ❌ list_package_management: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # install_package
    try:
        result = client.install_package('docassemble.demo')
        results['partial'].append('install_package')
        print(f"   ⚠️ install_package (partial - demo package)")
    except Exception as e:
        results['not_working'].append(('install_package', str(e)[:100]))
        print(f"   ❌ install_package: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # uninstall_package
    try:
        result = client.uninstall_package('nonexistent.package')
        results['partial'].append('uninstall_package')
        print(f"   ⚠️ uninstall_package (partial - test package)")
    except Exception as e:
        results['not_working'].append(('uninstall_package', str(e)[:100]))
        print(f"   ❌ uninstall_package: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # update_package
    try:
        result = client.update_package('docassemble.demo')
        results['partial'].append('update_package')
        print(f"   ⚠️ update_package (partial - demo package)")
    except Exception as e:
        results['not_working'].append(('update_package', str(e)[:100]))
        print(f"   ❌ update_package: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # restart_server
    try:
        result = client.restart_server()
        results['partial'].append('restart_server')
        print(f"   ⚠️ restart_server (partial - admin required)")
    except Exception as e:
        results['not_working'].append(('restart_server', str(e)[:100]))
        print(f"   ❌ restart_server: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # update_packages
    try:
        result = client.update_packages()
        results['partial'].append('update_packages')
        print(f"   ⚠️ update_packages (partial - admin required)")
    except Exception as e:
        results['not_working'].append(('update_packages', str(e)[:100]))
        print(f"   ❌ update_packages: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # 5. CONFIGURATION ENDPOINTS
    print(f"\n⚙️ CONFIGURATION (8 Endpunkte)")
    
    # get_configuration
    try:
        result = client.get_configuration()
        results['working'].append('get_configuration')
        print(f"   ✅ get_configuration")
    except Exception as e:
        results['not_working'].append(('get_configuration', str(e)[:100]))
        print(f"   ❌ get_configuration: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # set_configuration
    try:
        result = client.set_configuration({'test_setting': 'test_value'})
        results['partial'].append('set_configuration')
        print(f"   ⚠️ set_configuration (partial - admin required)")
    except Exception as e:
        results['not_working'].append(('set_configuration', str(e)[:100]))
        print(f"   ❌ set_configuration: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # get_cloud_configuration
    try:
        result = client.get_cloud_configuration()
        results['working'].append('get_cloud_configuration')
        print(f"   ✅ get_cloud_configuration")
    except Exception as e:
        results['not_working'].append(('get_cloud_configuration', str(e)[:100]))
        print(f"   ❌ get_cloud_configuration: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # set_cloud_configuration
    try:
        result = client.set_cloud_configuration({'test_cloud': 'test_value'})
        results['partial'].append('set_cloud_configuration')
        print(f"   ⚠️ set_cloud_configuration (partial - admin required)")
    except Exception as e:
        results['not_working'].append(('set_cloud_configuration', str(e)[:100]))
        print(f"   ❌ set_cloud_configuration: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # send_email
    try:
        result = client.send_email(['test@example.com'], 'Test Subject', 'Test Body')
        results['working'].append('send_email')
        print(f"   ✅ send_email")
    except Exception as e:
        results['not_working'].append(('send_email', str(e)[:100]))
        print(f"   ❌ send_email: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # send_sms
    try:
        result = client.send_sms('+1234567890', 'Test SMS')
        results['working'].append('send_sms')
        print(f"   ✅ send_sms")
    except Exception as e:
        results['not_working'].append(('send_sms', str(e)[:100]))
        print(f"   ❌ send_sms: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # get_redirect_url
    try:
        result = client.get_redirect_url('https://example.com')
        results['working'].append('get_redirect_url')
        print(f"   ✅ get_redirect_url")
    except Exception as e:
        results['not_working'].append(('get_redirect_url', str(e)[:100]))
        print(f"   ❌ get_redirect_url: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # get_credentials
    try:
        result = client.get_credentials('test_service')
        results['working'].append('get_credentials')
        print(f"   ✅ get_credentials")
    except Exception as e:
        results['not_working'].append(('get_credentials', str(e)[:100]))
        print(f"   ❌ get_credentials: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # 6. UTILITY ENDPOINTS
    print(f"\n🔧 UTILITY (16 Endpunkte)")
    
    # get_api_version
    try:
        result = client.get_api_version()
        results['working'].append('get_api_version')
        print(f"   ✅ get_api_version")
    except Exception as e:
        results['not_working'].append(('get_api_version', str(e)[:100]))
        print(f"   ❌ get_api_version: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # get_server_version
    try:
        result = client.get_server_version()
        results['working'].append('get_server_version')
        print(f"   ✅ get_server_version")
    except Exception as e:
        results['not_working'].append(('get_server_version', str(e)[:100]))
        print(f"   ❌ get_server_version: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # get_health_status
    try:
        result = client.get_health_status()
        results['working'].append('get_health_status')
        print(f"   ✅ get_health_status")
    except Exception as e:
        results['not_working'].append(('get_health_status', str(e)[:100]))
        print(f"   ❌ get_health_status: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # get_system_info
    try:
        result = client.get_system_info()
        results['working'].append('get_system_info')
        print(f"   ✅ get_system_info")
    except Exception as e:
        results['not_working'].append(('get_system_info', str(e)[:100]))
        print(f"   ❌ get_system_info: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # execute_python_code
    try:
        result = client.execute_python_code('print("Hello World")')
        results['working'].append('execute_python_code')
        print(f"   ✅ execute_python_code")
    except Exception as e:
        results['not_working'].append(('execute_python_code', str(e)[:100]))
        print(f"   ❌ execute_python_code: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # search_database
    try:
        result = client.search_database('test_table')
        results['working'].append('search_database')
        print(f"   ✅ search_database")
    except Exception as e:
        results['not_working'].append(('search_database', str(e)[:100]))
        print(f"   ❌ search_database: {str(e)[:50]}...")
    results['total_tested'] += 1
    
    # Weitere Utility-Endpunkte...
    utility_endpoints = [
        'export_interview_data', 'import_interview_data', 'backup_database',
        'restore_database', 'validate_yaml_syntax', 'format_yaml_content',
        'get_interview_metadata', 'set_interview_metadata', 'stash_data',
        'retrieve_stashed_data'
    ]
    
    for endpoint in utility_endpoints:
        try:
            if endpoint == 'stash_data':
                result = client.stash_data({'test': 'data'}, 'test_secret')
            elif endpoint == 'retrieve_stashed_data':
                result = client.retrieve_stashed_data('test_key', 'test_secret')
            elif endpoint == 'validate_yaml_syntax':
                result = client.validate_yaml_syntax('test: value')
            elif endpoint == 'format_yaml_content':
                result = client.format_yaml_content('test:value')
            elif endpoint == 'export_interview_data':
                result = client.export_interview_data('test_format')
            elif endpoint == 'import_interview_data':
                result = client.import_interview_data(b'test_data', 'test_format')
            elif endpoint == 'backup_database':
                result = client.backup_database()
            elif endpoint == 'restore_database':
                result = client.restore_database(b'test_backup')
            elif endpoint == 'get_interview_metadata':
                result = client.get_interview_metadata('docassemble.demo:data/questions/questions.yml')
            elif endpoint == 'set_interview_metadata':
                result = client.set_interview_metadata('docassemble.demo:data/questions/questions.yml', {'test': 'meta'})
            
            results['working'].append(endpoint)
            print(f"   ✅ {endpoint}")
        except Exception as e:
            results['not_working'].append((endpoint, str(e)[:100]))
            print(f"   ❌ {endpoint}: {str(e)[:50]}...")
        results['total_tested'] += 1
    
    # FINAL SUMMARY
    print(f"\n" + "="*60)
    print(f"📊 VOLLSTÄNDIGER TEST-REPORT")
    print(f"="*60)
    
    working_count = len(results['working'])
    partial_count = len(results['partial'])
    not_working_count = len(results['not_working'])
    total_count = results['total_tested']
    
    print(f"📈 GESAMTERGEBNIS:")
    print(f"   ✅ Funktionierend:     {working_count:2d}/{total_count} ({working_count/total_count*100:.1f}%)")
    print(f"   ⚠️ Teilweise:          {partial_count:2d}/{total_count} ({partial_count/total_count*100:.1f}%)")
    print(f"   ❌ Nicht funktionierend: {not_working_count:2d}/{total_count} ({not_working_count/total_count*100:.1f}%)")
    
    print(f"\n✅ FUNKTIONIERENDE ENDPUNKTE ({working_count}):")
    for endpoint in results['working']:
        print(f"   - {endpoint}")
    
    print(f"\n⚠️ TEILWEISE FUNKTIONIEREND ({partial_count}):")
    for endpoint in results['partial']:
        print(f"   - {endpoint}")
    
    print(f"\n❌ NICHT FUNKTIONIERENDE ENDPUNKTE ({not_working_count}):")
    for endpoint, error in results['not_working']:
        print(f"   - {endpoint}: {error[:60]}{'...' if len(error) > 60 else ''}")
    
    # Kategorisierung der Probleme
    print(f"\n🔍 PROBLEM-KATEGORISIERUNG:")
    
    session_errors = [e for e, err in results['not_working'] if 'session' in err.lower() or 'Unable to obtain interview dictionary' in err]
    api_errors = [e for e, err in results['not_working'] if '404' in err or 'Not Found' in err]
    permission_errors = [e for e, err in results['not_working'] if 'permission' in err.lower() or 'privilege' in err.lower()]
    file_errors = [e for e, err in results['not_working'] if 'file' in err.lower() and 'upload' in err.lower()]
    
    if session_errors:
        print(f"   🔄 Session-Probleme ({len(session_errors)}): {', '.join(session_errors[:3])}{'...' if len(session_errors) > 3 else ''}")
    if api_errors:
        print(f"   🚫 API nicht verfügbar ({len(api_errors)}): {', '.join(api_errors[:3])}{'...' if len(api_errors) > 3 else ''}")
    if permission_errors:
        print(f"   🔐 Berechtigungsfehler ({len(permission_errors)}): {', '.join(permission_errors[:3])}{'...' if len(permission_errors) > 3 else ''}")
    if file_errors:
        print(f"   📁 Datei-Upload-Probleme ({len(file_errors)}): {', '.join(file_errors[:3])}{'...' if len(file_errors) > 3 else ''}")
    
    return results

if __name__ == "__main__":
    test_all_endpoints()
