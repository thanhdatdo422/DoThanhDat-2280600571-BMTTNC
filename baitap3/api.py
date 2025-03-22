import os
from flask import Flask, request, jsonify
from cipher.rsa import RSACipher
from cipher.ecc import ECCCipher

app = Flask(__name__)

# RSA CIPHER ALGORITHM
rsa_cipher = RSACipher()

@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route('/api/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    data = request.json
    message = data.get('message')
    key_type = data.get('key_type')

    keys = rsa_cipher.load_keys()
    if not keys or len(keys) != 2:
        return jsonify({'error': 'Key loading failed'}), 500
    private_key, public_key = keys

    key = public_key if key_type == 'public' else private_key if key_type == 'private' else None
    if key is None:
        return jsonify({'error': 'Invalid key type'}), 400

    encrypted_message = rsa_cipher.encrypt(message, key)
    return jsonify({'encrypted_message': encrypted_message.hex()})

@app.route('/api/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    data = request.json
    ciphertext_hex = data.get('ciphertext')
    key_type = data.get('key_type')

    keys = rsa_cipher.load_keys()
    if not keys or len(keys) != 2:
        return jsonify({'error': 'Key loading failed'}), 500
    private_key, public_key = keys

    key = public_key if key_type == 'public' else private_key if key_type == 'private' else None
    if key is None:
        return jsonify({'error': 'Invalid key type'}), 400

    ciphertext = bytes.fromhex(ciphertext_hex)
    decrypted_message = rsa_cipher.decrypt(ciphertext, key)
    return jsonify({'decrypted_message': decrypted_message})

@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json
    message = data.get('message')

    keys = rsa_cipher.load_keys()
    if not keys or len(keys) != 2:
        return jsonify({'error': 'Key loading failed'}), 500
    private_key, _ = keys

    signature = rsa_cipher.sign(message, private_key)
    return jsonify({'signature': signature.hex()})

@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json
    message = data.get('message')
    signature_hex = data.get('signature')

    keys = rsa_cipher.load_keys()
    if not keys or len(keys) != 2:
        return jsonify({'error': 'Key loading failed'}), 500
    _, public_key = keys

    signature = bytes.fromhex(signature_hex)
    is_verified = rsa_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

# ECC CIPHER ALGORITHM
ecc_cipher = ECCCipher()

@app.route('/api/ecc/generate_keys', methods=['GET'])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json
    message = data.get('message')

    keys = ecc_cipher.load_keys()
    if not keys or len(keys) != 2:
        return jsonify({'error': 'Key loading failed'}), 500
    private_key, _ = keys

    signature = ecc_cipher.sign(message, private_key)
    return jsonify({'signature': signature.hex()})

@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify_signature():
    data = request.json
    message = data.get('message')
    signature_hex = data.get('signature')

    keys = ecc_cipher.load_keys()
    if not keys or len(keys) != 2:
        return jsonify({'error': 'Key loading failed'}), 500
    _, public_key = keys

    signature = bytes.fromhex(signature_hex)
    is_verified = ecc_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

# Main function
if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
