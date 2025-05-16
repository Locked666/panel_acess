from werkzeug.security import generate_password_hash, check_password_hash

if __name__ == '__main__':
    pas = generate_password_hash('123456789', method='pbkdf2:sha256')
    print(pas)
    
    spas = check_password_hash(pas, '123456789')
    print(spas)