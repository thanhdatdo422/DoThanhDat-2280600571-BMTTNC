from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

def generate_dh_paramenters():
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    return parameters

def generate_sever_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def main():
    parameters = generate_dh_paramenters()
    private_key, public_key = generate_sever_key_pair(parameters)
    
    with open("server_public_key.pem","wb") as f:
        f.write(public_key.public_bytes
                (encoding=serialization.Encoding.PEM, 
                 format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
if __name__ == "__main__":
    main()