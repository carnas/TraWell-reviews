PUBLIC_KEY = '-----BEGIN RSA PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsigrn1IczQr4Ywmd+30WkyQAAV6tih58ENcCikivikUdLWN1HBWNjU53US9YXiJThpSNXSKeRMJ95f9OWj4uaCHIeN4hKrOsdnLoETiaDEGrKymzcLFHBhaVK7Cpna3zUUJWDajRjlmNHvLa+8IIApeF0e5pLCgXbeGyxnSmLhrhftVmuKJ2xEeAul/nQV3UGD+Qg/sKTpI7wdDARhOaQ0EjX/gO7uYKQ+pDVwlfgFDuJaJ/LjgQpe4zRNS3VD8X5lV+uQFkTJC2OQlPEunRFjQe6s/iR2IEGwNx3oISwCZsm7FyGZ1wTnCqO4rq39PkffRSA696HfJDszGo6c6hyQIDAQAB\n-----END RSA PUBLIC KEY-----'
ISSUER_CLAIM = 'http://localhost:8403/auth/realms/TraWell'
ALGORITHMS = ['RS256']
JWT_OPTIONS = {
        'verify_signature': False,
        'verify_exp': True,
        'verify_iss': True,
        'verify_iat': True,
        'verify_aud': False,
    }