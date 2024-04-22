from flask import Flask,redirect,url_for,render_template,request
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb+srv://test:sparta@cluster0.vmgfjkn.mongodb.net/?retryWrites=true&w=majority')
db = client.dbbuah

app=Flask(__name__)
@app.route('/',methods=['GET'])
def home():
    return render_template('dashboard.html')

@app.route('/fruit',methods=['GET'])
def fruit():
    fruit = list(db.fruit.find({}))
    return render_template('index.html', fruit = fruit)

@app.route('/addfruit',methods=['GET','POST'])
def addfruit():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        desc = request.form['deskripsi']
        gambar = request.files['gambar']
        
        if gambar:
            namaGambarAsli = gambar.filename
            namafileGambar = namaGambarAsli.split('/')[-1]
            file_path = f'static/assets/imgGambar/{namafileGambar}'
            gambar.save(file_path)
        
        else:
            gambar = None
        
        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': desc,
            'gambar': namafileGambar
        }
        db.fruit.insert_one(doc)
        return redirect(url_for("fruit"))
    return render_template('addFruit.html')

@app.route('/editfruit/<_id>',methods=['GET','POST'])
def editfruit(_id):
    if request.method == 'POST':
        id = request.form['_id']
        nama = request.form['nama']
        harga = request.form['harga']
        desc = request.form['deskripsi']
        gambar = request.files['gambar']

        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': desc,
        }
        
        if gambar:
            namaGambarAsli = gambar.filename
            namafileGambar = namaGambarAsli.split('/')[-1]
            file_path = f'static/assets/imgGambar/{namafileGambar}'
            gambar.save(file_path)
            doc['gambar'] = namafileGambar
        db.fruit.update_one({"_id":ObjectId(_id)},{"$set":doc})
        return redirect(url_for("fruit"))

    id = ObjectId(_id)
    data = list(db.fruit.find({"_id": id}))
    return render_template('EditFruit.html', data = data)

@app.route('/delete/<_id>',methods=['GET'])
def delete(_id):
    db.fruit.delete_one({"_id": ObjectId(_id)})
    
    return redirect(url_for("fruit"))

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)