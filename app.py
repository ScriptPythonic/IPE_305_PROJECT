from website import Create_app
app=Create_app()

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=3000)
