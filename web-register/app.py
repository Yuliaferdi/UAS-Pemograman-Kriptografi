from flask import Flask, render_template, request, redirect, url_for, session
import string
import random

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(24))

# Fungsi enkripsi Caesar
def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Enkripsi password dengan metode Caesar
    encrypted_password = caesar_cipher(password, shift=3)

    # Simpan hasil login yang sudah dienkripsi (simpan ke file)
    save_to_file(f"Username: {username}, Encrypted Password: {encrypted_password}")

    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Enkripsi password dengan metode Caesar
    encrypted_password = caesar_cipher(password, shift=3)

    if is_valid_user(username, encrypted_password):
        # Tanda bahwa pengguna berhasil login
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', login_error=True)

@app.route('/dashboard')
def dashboard():
    # Periksa apakah pengguna berhasil login
    if 'logged_in' in session and session['logged_in']:
        return 'Welcome to the Dashboard!'
    else:
        return redirect(url_for('home'))

def save_to_file(data):
    with open('login_results.txt', 'a') as file:
        file.write(data + '\n')

def is_valid_user(username, encrypted_password):
    return True

if __name__ == '__main__':
    app.run(debug=True)
