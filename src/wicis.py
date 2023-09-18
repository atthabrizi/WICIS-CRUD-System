from tabulate import tabulate
import os
import csv
import time
import getpass
import pyinputplus as pyip

# all about data (csv.)
def get_db():
    """
    Fungsi ini digunakan untuk extract data dari csv sebagai reader ('r')
    Returns:
        dict: database sementara (untuk program)
    """
    # membuat dict database kosong untuk mengextract data
    database = {}
    global PATH
    PATH = r'C:\Users\attha\OneDrive\Documents\Dokumen Sementara (Nanti pindah hardisk)\Purwadhika JCDS-02\Capstone Projects\Module 1 - Programming\Reproject-Mode Malathi\data\data_prod.csv'
    with open(PATH, 'r') as file:
        # 
        dataReader = csv.reader(file, delimiter=";")
        # Input row into dictionary
        for i, row in enumerate(dataReader): # enumerate untuk meminsahkan header dan isi
            # For header
            if i == 0:
                header = row
                database.update({"column": header})
                continue
            # For data
            prod_id, name, brand, series, type, qty, price, cogs = row
            database.update({prod_id: [prod_id, name, brand, series, type, int(qty), int(price), int(cogs)]})

    return database
def save(database):
     with open(PATH, 'w', newline='') as file:
        dataWriter = csv.writer(file, delimiter=';')
        dataWriter.writerows(database.values())  

#initiate login
def loginput(max_attemps=3): 
    global accountDict
    accountDict = {
    'alyaa': {'position': 'owner', 'code': 'obpalya'},
    'icha': {'position': 'owner', 'code': 'bbicha'},
    'anggrek': {'position': 'cashier', 'code': 'anggrek'},
    'melati': {'position': 'cashier', 'code': 'melati'}}

    header = '''
    atthabrizi@gmail.com
    ======= WICIS =======
    Terimakasih telah menggunakan WICIS!
    Program ini dibuat untuk membantu UMKM dalam integrasi pengelolaan
    stok dan medium pembelian. 

    Usaha anda terdaftar sebagai:
    CV Mode Malathi Mahakarya
    Retail Fashion Company


    Klik M untuk memulai dan X untuk keluar dari program.

    IMPORTANT NOTE:
    Untuk melakukan Exit program hanya bisa dilakukan melalui
    Menu ini. untuk mengakses kembali laman ini bisa dengan
    menginput kode Logout pada Main Menu
    Data yang telah diubah akan otomatis tersimpan
    pada file csv setelah mengetik X pada Menu ini.


    =====================
    '''
    clear_screen()
    print(header)
    inorout = pyip.inputChoice(prompt='Input Option Code : ',choices=['M','X'])
    print(inorout)
    if inorout == 'M':
        clear_screen()
        print(header.center(1))
        attemps = 0
        while attemps < max_attemps:
            user = input("Enter your username: ")
            Pass = getpass.getpass("Type in your password: ")

            if user in accountDict and Pass == accountDict[user]['code']:
                global using, posisi, password  # buat pembeda nanti
                using = user
                posisi = accountDict[user]['position']
                password = accountDict[user]['code']
                print(f'''Login berhasil!

    Halo!

        Nama = {using}
        Status = {posisi}

    Selamat menggunakan! 
    ======= RICIS =======''')
                return MainMenu()
            else:
                print('Login gagal! Nama atau password anda belum terdaftar dalam direktori!')
                attemps += 1
                print(f'\nSilahkan coba ulang! \n No. of attemps {attemps}/{max_attemps}')
        else:
            print("Anda sudah mencapai batas login! Anda bisa mencoba lagi setelah 30 detik!")
            time.sleep(30)
            print(input('''
                ======Silahkan Login Ulang!======

                Ketik ENTER untuk Login Ulang'''))

            loginput()
    if inorout == 'X':
        save(database)
        print('Data yang anda ubah telah disimpan, ketik ENTER untuk meninggalkan program!\n')
        enter()
        quit
    return quit

# fungsi extensi
def clear_screen():
    """
    A function to clean the user interface
    """
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')
def enter():
    inputenter = input("Ketik ENTER untuk melanjutkan!")
    print(inputenter)
def printInvent(database):
    # tes tabulate
    header = database['column']
    data = list(database.values())[0:]
    data = data[1:]
    print(tabulate(data,header,tablefmt='fancy_grid'), '\n')
def tabul(database):
    listtable = list(database.values())
    print(tabulate(listtable,headers='firstrow',tablefmt='fancy_grid'))

# Read Function
def ShowInvent(database):
    # Local function
    def ShowMenu(database):
        if posisi == 'owner':
            header =''' 
    
    Apakah anda ingin merubah produk?
        
    A. Add New Product Inventory
    B. Remove Product from Inventory
    C. Change Data from Inventory
    E. Access Show Inventory Menu
    M. Kembali ke Main Menu

        ======================================================
              
              '''
            print(header)
            access = pyip.inputChoice(prompt='Input Option Code = ', choices=['A','B','C','E','M'])
            if access == 'A':
                addProduct(database)
            elif access == 'B':
                delProduct(database)
            elif access == 'C':
                updProduct(database)
            elif access == 'E':
                ShowInvent(database)
            elif access == 'M':
                MainMenu()
        elif posisi == 'cashier':
            header =''' 

    M. Kembali ke Main Menu
    E. Akses Mode Cashier 

        ======================================================
              
              '''
            print(header)
            access = pyip.inputChoice(prompt='Input Option Code = ', choices=['E','M'])
            if access == 'E':
                cashier(database)
            elif access == 'M':
                MainMenu()

    
    def AllData(database):
        clear_screen()
        print('''
        ====== INVENTORY CV MODE MALATHI MAHAKARYA ======''')
        printInvent(database)
        ShowMenu(database)
    def ShowBrand(database):
        clear_screen()
        inputBrand = pyip.inputChoice(prompt='Input nama brand [OBP/BB] = ', choices=['OBP','BB'])
        if inputBrand == 'OBP':
            filteredList = {k: v for k, v in database.items() if v[2] == 'OBP'}
            header = ['ProductID', 'Nama Product', 'Brand', 'Series', 'Type', 'Qty', 'Harga', 'COGS']
            tableOBP = [header] + [filteredList[key] for key in filteredList] # list comprehensions
            print('''
        ====== INVENTORY CV MODE MALATHI MAHAKARYA ======''')
            print(tabulate(tableOBP, headers='firstrow', tablefmt='grid'))
            ShowMenu(database)
        elif inputBrand == 'BB':
            filteredList = {k: v for k, v in database.items() if v[2] == 'BB'}
            header = ['ProductID', 'Nama Product', 'Brand', 'Series', 'Type', 'Qty', 'Harga', 'COGS']
            tableOBP = [header] + [filteredList[key] for key in filteredList] # list comprehensions
            print('''
        ====== INVENTORY CV MODE MALATHI MAHAKARYA ======''')
            print(tabulate(tableOBP, headers='firstrow', tablefmt='grid'))
            ShowMenu(database)            
    def ShowSeries(database):
        clear_screen()
        printInvent(database)
        inputBrand = pyip.inputStr(prompt='Input nama Series : ')
        filteredList = {k: v for k, v in database.items() if v[3] == inputBrand.capitalize()}
        header = ['ProductID', 'Nama Product', 'Brand', 'Series', 'Type', 'Qty', 'Harga', 'COGS']
        tableSeries = [header] + [filteredList[key] for key in filteredList] # list comprehensions
        print('''
        ====== INVENTORY CV MODE MALATHI MAHAKARYA ======''')
        print(tabulate(tableSeries, headers='firstrow', tablefmt='fancy_grid'))
        ShowMenu(database)
    def ShowType(database):
        clear_screen()
        printInvent(database)
        types = ['Atasan','Bawahan','Aksesoris','Raw']

        inputType = pyip.inputChoice(prompt='Input nama Type : ',choices=types)
        filteredList = {k: v for k, v in database.items() if v[4] == inputType.capitalize()}
        header = ['ProductID', 'Nama Product', 'Brand', 'Series', 'Type', 'Qty', 'Harga', 'COGS']
        tableSeries = [header] + [filteredList[key] for key in filteredList] # list comprehensions
        print('''
        ====== INVENTORY CV MODE MALATHI MAHAKARYA ======''')
        print(tabulate(tableSeries, headers='firstrow', tablefmt='fancy_grid'))
        ShowMenu(database)

    # Main Show Program
    clear_screen()
    header = '''
    ======= WICIS =======
        Show Database
          
    Pada fitur ini anda bisa mengakses database product
    yang ada. Anda bisa mengakses berdasarkan brand dan
    series yang anda inginkan.
          
    A. Show All Inventory Data
    B. Show Data Based on Brand
    C. Show Data Based on Series
    D. Show Data Based on Types

    Anda juga bisa mengakses data penjualan dengan 
    input code 'O'
          
    Fitur ini hanya dapat digunakan oleh user dengan status 
    'owner'. Apabila anda tidak termasuk user tersebut, silahkan
    Ketik 'M' dan kembali ke Menu Utama
          
    ================='''
    print(header)
    access = pyip.inputChoice(prompt='Input Option Code : ',choices=['A','B','C','D','O','M'])

    if access == 'A':
        AllData(database)
    elif access == 'B':
        ShowBrand(database)
    elif access == 'C':
        ShowSeries(database)
    elif access == 'D':
        ShowType(database)
    elif access == 'O':
        clear_screen()
        print("Under development")
        enter()
        MainMenu()
    elif access == 'M':
        MainMenu()

# Create Function
def addProduct(database):
    ''' 
    addProduct function ini digunakan untuk menambahkan produk baru kedalam direktori persediaan perusahaan.
    argument:
        database (products): database product inventory

    return:
        products: updated inventory database
    '''
    # Local function
    def addFunction():
        clear_screen()
        print('''
    ======= WICIS =======
        Add Data
              
              ''')
          
        newprod = {} # untuk menyetor data sementara
        newprod['Brand'] = pyip.inputChoice(prompt='Masukkan Brand dari product baru : ',choices=['OBP','BB'])
        newprod['Nama Product'] = pyip.inputStr(prompt='Nama Product : ')
        newprod['Series'] = pyip.inputStr(prompt='Nama Series : ')
        newprod['Type'] = pyip.inputStr(prompt='Nama Type : ')
        newprod['Qty'] = pyip.inputInt(prompt='Quantity : ')
        newprod['Harga'] = pyip.inputInt(prompt='Harga Jual : ')
        newprod['COGS'] = pyip.inputInt(prompt='Harga Beli (HPP) : ')
        newprod['ProductID'] = newprod['Brand'][:4] + newprod['Nama Product'][:2].upper() + newprod["Series"][:3].upper()
        margin = (newprod['Harga']-newprod["COGS"])/(newprod["COGS"])*100

        check = f'''
        === Silahkan cek ulang data yang telah anda masukkan ===
        ProductID = {newprod["ProductID"]}
        Nama product = {newprod["Nama Product"]}
        Nama Series = {newprod["Series"]}
        Type = {newprod["Type"]}
        Qty. = {newprod["Qty"]} pcs
        COGS = Rp. {newprod["COGS"]}
        Harga = Rp. {newprod["Harga"]}

        Profit Margin = {int(margin)} %

        '''
        print(check)   # cek validitas data
        
        valid = pyip.inputYesNo(prompt='''
        Ketik Y - Jika data anda sudah sesuai
        Ketik N - Jika anda ingin menginput data ulang 

        Apakah data anda sudah sesuai ? = ''')

        if valid == 'yes':
            passw = getpass.getpass('Masukkan password anda = ')
            attempts = 0
            while passw != password:
                attempts += 1
                print(f'Password yang anda masukkan salah! Attemps({attempts}/3)')
                passw = input('Masukkan password anda = ')
                if attempts >= 3:
                    print(input('Batas percobaan telah terlampaui! Ketik enter untuk mengulangi'))
                    clear_screen
                    addProduct()  

            print("\nPRODUCT BARU BERHASIL DIDAFTARKAN!\n")
                # append
            database[newprod['ProductID']] = [newprod['ProductID'],newprod['Nama Product'],
            newprod['Brand'],newprod['Series'],newprod['Type'],
            newprod['Qty'],newprod['Harga'],newprod['COGS']]
            clear_screen()
            print('''====== INVENTORY ====== ''')
            tabul(database)
            enter() # keluar dari loop
        else:
            addProduct(database)
        reAdd = pyip.inputChoice(prompt='''Apa anda ingin menambahkan data produk lagi?

                                 A. Saya ingin menambahkan Input
                                 B. Kembali ke Main Menu

                                 Input Option Code : ''',choices=['A','B'])
        if reAdd == 'A':
            addProduct(database)
        if reAdd == 'B':
            MainMenu()
    clear_screen()
    
    print('''
    ======= WICIS =======
        Add Data
          
    Pada fitur ini anda bisa menambahkan produk baru 
    pada database inventory anda. Untuk menginput data
    pastikan anda sudah mempersiapkan data dibawah ini:
          
          - Nama Brand (OBP/Bhasabhumi)
          - Nama Product
          - Nama Series
          - Tipe Produk (Atasan, Bawahan, Aksesoris..etc.)
          - Harga Beli (HPP)
          - Harga Jual 

    Input A pada Option Code untuk melanjutkan.
          
    Fitur ini hanya dapat digunakan oleh user dengan status 
    'owner'. Apabila anda tidak termasuk user tersebut, silahkan
    Ketik 'M' dan kembali ke Menu Utama
          
    =================
          
    ''')
    inputMenu = pyip.inputChoice(prompt='Input Option Code : ', choices=['M','A'])
    print(inputMenu)

    if inputMenu == 'M':
        MainMenu()
    elif inputMenu == 'A':
        addFunction()

# Update Function
def updProduct(database):
    ''' 
    updProduct function ini digunakan untuk mengubah data produk yang ada pada direktori persediaan perusahaan.
    argument:
        database (products): database product inventory

    return:
        products: updated product database
    '''
    # local function
    def updFunction(database):
        clear_screen()
        header = '''
    ======= WICIS =======
        Update Data
              
              '''
        print(header)
        
        printInvent(database)
        prodKeys = list(database.keys()) + ['M']
        brandID = pyip.inputChoice(prompt='Masukkan Brand ID dari data yang ingin diubah:',choices=prodKeys)
        choice = database['column']
        
        if brandID == 'M':
            MainMenu()

        passw = getpass.getpass('Masukkan password anda = ')
        attempts = 0
        while passw != password:
            attempts += 1
            print(f'Password yang anda masukkan salah! Attemps({attempts}/3)')
            passw = input('Masukkan password anda = ')
            if attempts >= 3:
                print(input('Batas percobaan telah terlampaui! Ketik enter untuk mengulangi'))
                clear_screen
                MainMenu() 

    
        if brandID in database.keys():
            key = pyip.inputMenu(prompt='Input bagian yang ingin diubah?\n\n',choices=choice,numbered=True)
            print(key)
            if key == 'ProductID':
                newID = pyip.inputStr(prompt='Masukkan Product ID baru : ')
                database[brandID][0] = newID
            elif key == 'Nama Product':
                newName = pyip.inputStr(prompt='Masukkan Nama Product baru : ')
                database[brandID][1] = newName
            elif key == 'Brand':
                newBrand = pyip.inputChoice(prompt='Masukkan Brand baru (OBP/BB) : ',choices=['OBP','BB'])
                database[brandID][2] = newBrand
            elif key == 'Series':
                newSeries = pyip.inputStr(prompt='Masukkan Nama Series baru : ')
                database[brandID][3] = newSeries
            elif key == 'Type':
                newType = pyip.inputChoice(prompt='Masukkan Type Product baru [Atasan, Bawahan, Outer, Aksesoris, Raw]: ',choices=['Atasan', 'Bawahan', 'Outer', 'Aksesoris', 'Raw'])
                database[brandID][4] = newType
            elif key == 'Qty':
                newQty = pyip.inputInt(prompt='Masukkan Jumlah Product baru : ')
                database[brandID][5] = newQty
            elif key == 'Harga':
                newHarga = pyip.inputInt(prompt='Masukkan Harga Product baru : ')
                database[brandID][6] = newHarga
            elif key == 'COGS':
                newCOGS = pyip.inputInt(prompt='Masukkan HPP Product baru : ')
                database[brandID][7] = newCOGS
            
            print(tabulate([database[brandID]],database['column'],tablefmt='fancy_grid'))
        
            print('DATA TELAH BERHASIL DIUBAH!')

            quit = pyip.inputChoice(prompt='Apakah anda ingin mengubah bagian lain? ',choices=['Y','N'])
            if quit == 'Y':
                save(database)
                updFunction(database)
            else:
                save(database)
                updProduct(database)
                    
        print('====== UPDATED DATABASE ======')
        printInvent(database)
        enter()
        updFunction(database)


    clear_screen()
    print('''
    ======= WICIS =======
        Update Data
          
    Pada fitur ini anda bisa merubah atau melakukan 
    koreksi dari data produk yang sudah ada pada 
    database. 

    Input A pada Option Code untuk melanjutkan.
          
    Fitur ini hanya dapat digunakan oleh user dengan status 
    'owner'. Apabila anda tidak termasuk user tersebut, silahkan
    Ketik 'M' dan kembali ke Menu Utama
          
    =================
          
    ''')
    inputMenu = pyip.inputChoice(prompt='Input Option Code : ', choices=['M','A'])
    print(inputMenu)

    if inputMenu == 'M':
        MainMenu()
    elif inputMenu == 'A':
        updFunction(database)
        save(database)

# Delete Function
def delProduct(database):
    # Local function
    def delbyID(database):
        '''
        delete menggunakan productID'''
        clear_screen()
        header =  ('''
        ======= WICIS =======
            Delete a Product

            Pada fitur ini anda bisa menghapus produk yang sudah
            anda daftarkan pada database inventory anda menggunakan
            parameter 'ProductID'.

            Ketik A untuk melakukan penghapusan.

            Disclaimer:

            Fitur ini akan menghapus keseluruhan data dari sebuah 
            product yang anda input. 

            Untuk menghapus quantitas produk bisa dilakukan melalui
            fitur Update pada Main Menu. and bisa menginput option
            code sebagai 'M' dan kembali ke Menu Utama
        =====================
        ''')
        print(header)
        inputMenu = pyip.inputChoice(prompt='Input Option Code : ',choices=['A','M'])
        if inputMenu == 'A':
            clear_screen()
            print('====== PRODUCT DATABASE ======')
            printInvent(database)
            delID = input('Input ID dari Product yang ingin dihapus = ')
            if delID.upper() in database.keys():
                productFound = ('''
                  ====== PRODUCT DITEMUKAN ======''')
                print(productFound)
                print(tabulate([database[delID]],database['column'],tablefmt='fancy_grid'))
                
                check = pyip.inputYesNo(prompt="Apakah anda yakin ingin menghapus produk ini? (Y/N) :")
                if check == 'yes':
                    passw = getpass.getpass('Masukkan password anda = ')
                    attempts = 0
                    while passw != password:
                        attempts += 1
                        print(f'Password yang anda masukkan salah! Attempts ({attempts}/3)')
                        passw = input('Masukkan password anda = ')
                        if attempts >= 3:
                            input('Batas percobaan telah terlampaui! Ketik enter untuk mengulangi')
                            clear_screen()
                            delProduct(database)  
                    else:
                        clear_screen()
                        print('====== PRODUCT DATABASE ======')
                        printInvent(database)
                        print(productFound)
                        del database[delID.upper()]
                        print("\nPRODUCT BERHASIL DIHAPUS!\n")
                        newdatabase = input('Tekan ENTER untuk melihat database baru : ')
                        print(newdatabase)
                        clear_screen()
                        print('====== UPDATED DATABASE ======')
                        printInvent(database)
                        enter()
                        delbyID(database)
            else:
                print('\n PRODUCT TIDAK DITEMUKAN \n')
                enter()
                delbyID(database)
        else: 
            MainMenu()
        return(database)
    

    # Main Delete Program
    clear_screen()
    header =  ('''
    ======= WICIS =======
        Remove Data
        
        Pada fitur ini anda bisa menghapus produk yang sudah
        anda daftarkan pada database inventory anda. 
        Anda bisa melakukan penghapusan berdasarkan Series 
        ataupun product satuan.
               
               
        Untuk menghapus quantitas produk bisa dilakukan melalui
        fitur Update pada Main Menu.
               
        Input A untuk menggunakan fitur ini.

        Fitur ini hanya dapat digunakan oleh user dengan status 
        'owner'. Apabila anda tidak termasuk user tersebut, silahkan
        Ketik 'M' dan kembali ke Menu Utama
    =====================
    ''')
    print(header)
    menu = pyip.inputChoice(prompt = 'Input Option Code = ',choices=['A','M'])
    
    if menu == 'A':
        delbyID(database)
        delProduct(database)
    elif menu == 'M':
        MainMenu()
    return database

# Cashier funtion (Update Function extension)
def cashier(database):
        cart = {} # [BrandID] : [ProductID;Nama Product;Brand;Series;Type;Qty;Harga;COGS]
        def addItem(database,cart):
            clear_screen()
            print('===CART===')
            print(tabulate(cart.items(),headers=['ProductID','Qty'],tablefmt='fancy_grid'))
            print('======INVENTORY======')
            printInvent(database)
            choice = list(database.keys()) + ['B']
            brandID = pyip.inputChoice(prompt='Klik B untuk Checkout\nEnter BrandID : ',choices=choice)
            if brandID == 'B':
                checkout(database,cart)
            quant = pyip.inputInt('Jumlah item : ')
            totalPrice = quant * database[brandID][6]
            validate = f'''
            Anda akan memasukkan item ini kedalam keranjang

            ProductID       : {database[brandID][0]}
            Nama Product    : {database[brandID][1]}

            Harga           : {database[brandID][6]}
            Jumlah          : {quant}
            Total Harga     : {totalPrice}

            ==========

            Ketik A untuk menambahkan ke keranjang.
            Ketik F untuk membatalkan.'''
            print(validate)
            inputMenu = pyip.inputChoice(prompt='Input Option Code : ',choices=['A','F'])
            while True:
                if inputMenu == 'A':
                    if brandID in cart:
                        cart[brandID] += quant
                    else:
                        cart[brandID] = quant
                    print(tabulate(cart.items(),tablefmt='fancy_grid'))

                    addItem(database,cart)
                elif inputMenu == 'F':
                    break         
        def checkout(database,cart):
            clear_screen()
            print('=== Berikut adalah item pada keranjang anda ===')
            print(tabulate(cart.items(),tablefmt='fancy_grid'))
            print('''
        Berikut adalah barang yang ada pada keranjang anda.
                  
        Klik A untuk checkout
        Klik B untuk menambahkan item.
        Klik F untuk membatalkan.
                  ''')
            inputMenu = pyip.inputChoice(prompt='Input Option Code : ',choices=['A','B','F'])
            
            if inputMenu == 'A':
                totalPrice = 0
                clear_screen()
                print('======INVOICE======')
                for brandID, quant in cart.items():
                    product = database[brandID]
                    itemPrice = quant * product[6]
                    totalPrice += itemPrice
                    print(f'''{product[1]} ({product[2]}) 
                          - Jumlah: {quant} 
                          - Total Harga: {itemPrice}''')
                finalize = pyip.inputChoice(prompt='Ketik A untuk checkout\n Ketik F untuk membatalkan : ',choices=['A','F'])
                if finalize == 'A':
                    # update inventory 
                    for brandID, quant in cart.items():
                     q = database[brandID][5]
                     q -= quant
                    print(f'Total Belanja Anda: {totalPrice}')
                    MainMenu()
                    print(input('Terima kasih atas pembelian Anda!'))
                    addItem(database)
                if finalize == 'F':
                    MainMenu()  
            elif inputMenu == 'B':
                addItem(database)
            elif inputMenu == 'F':
                cashier(database)
            
        header =  ('''
        ======= WICIS =======
            Cashier Dashboard


            Fitur ini digunakan untuk kasir melakukan checkout
            dimana pembelian bisa dilakukan terhadap produk 
            persediaan yang sudah ada.

            Untuk fitur ini akan menggunakan input ProductID
            yang nanti juga akan ditampilkan beserta data
            produk lainnya

            Fitur ini hanya dapat digunakan oleh user dengan status 
            'owner' maupun 'cashier'.
            Ketik 'A' untuk menggunakan fitur ini.
            Ketik 'M' dan kembali ke Menu Utama.
        =====================
        ''')
        clear_screen()
        print(header)    
        cashier = pyip.inputChoice(prompt='Enter Input Code : ', choices=['A','M'])
        clear_screen()

        if cashier == 'M':
            MainMenu
        elif cashier == 'A':
            printInvent(database)
            print('''
            ================

            A. Masukan Item kedalam Keranjang
            B. Checkout 
            M. Kembali ke Main Menu

            ================
                  ''')

            buyID = pyip.inputChoice(prompt='Enter Input Code : ', choices=['A','B','M'])
            if buyID == 'A':
                addItem(database,cart)
                save(database)
            elif buyID == 'B':
                checkout()
            elif buyID == 'M':
                MainMenu()

        header =  ('''
        ======= WICIS =======
            Cashier Dashboard


            Fitur ini digunakan untuk kasir melakukan checkout
            dimana pembelian bisa dilakukan terhadap produk 
            persediaan yang sudah ada.

            Untuk fitur ini akan menggunakan input ProductID
            yang nanti juga akan ditampilkan beserta data
            produk lainnya

            Fitur ini hanya dapat digunakan oleh user dengan status 
            'owner' maupun 'cashier'.
            Ketik 'A' untuk menggunakan fitur ini.
            Ketik 'M' dan kembali ke Menu Utama.
        =====================
        ''')

# readme inside program
def information():
    clear_screen()
    info = '''
======= WICIS =======
          
Widely Integrated Cashier and Inventory System (WICIS) adalah sebuah project platform
yang ditujukan untuk membantu sistem penyimpanan database persediaan yang menyediakan
sistem Create, Read, Update and Delete (CRUD) menggunakan sistem cashier.

Untuk menggunakan WICIS, diperlukan login access bagi user yang sudah terdaftar. User
akan memiliki dua macam status, yaitu owner dan cashier. Dimana owner memiliki akses
semua fitur CRUD dan fitur untuk menambahkan login access kepada user baru.

Untuk user dengan status cashier bisa mengaksaes fitur Show dan Delete hanya melalui 
mode cashier dimana user bisa melakukan check-out.

Berikut adalah beberapa fitur yang bisa anda gunakan:

- Show Current Inventory Data
- Add New Product Inventory
- Remove Product from Inventory
- Renew Data from Inventory
- Cashier Mode

Untuk memberikan feedback ataupun pertanyaan lebih dalam mohon hubungi
atthabrizi@gmail.com

=======================

M. Back to Main Menu
X. Login Access
Y. Your Info

'''
    print(info)
    access = pyip.inputChoice(
        prompt='Enter feature code = \n', 
        choices=['M','X','Y'])
    
    if access == 'M':
        MainMenu()
    elif access == 'X':
        loginput() # nanti ganti fitur login access
    elif access == 'Y':
        clear_screen()
        print(f'''
===== YOUR INFO =====
Username : {using}
Status : {posisi}\n''')
        enter()
        clear_screen()
        information()

    else:
        information()

# Main Menu
def MainMenu():           
        '''
    Ini main menu dimana akan digunakan sebagai workspace untuk mengakses fitur2
    
    Argument=
    login first


        Return=
        Create - addProduct()
        Read - showProduct()
        Update - updateProduct()
        Delete - delete() and cashier()

        '''
        header = f''' 
            ======= MENU UTAMA =======
        
            Halo, {using.capitalize()} Status: {posisi}
            Terimakasih telah menggunakan WICIS!
            Program ini dibuat untuk membantu UMKM dalam integrasi pengelolaan 
            stok dan medium pembelian. 
        
            Usaha anda terdaftar sebagai:
            CV Mode Malathi Mahakarya
            Retail Fashion Company
        
            Berikut adalah beberapa fitur yang bisa anda gunakan:
        
            A. Show Current Inventory Data
            B. Add New Product Inventory
            C. Remove Product from Inventory
            D. Change Data from Inventory
            E. Cashier Mode
        
            =======================
        
            L. Logout
            I. Information
        
            '''

        def menuOwner():
            clear_screen()
            print(header)
            access = pyip.inputChoice(
                prompt=("\nInput Option Code = \n"), 
                choices= ['A','B','C','D','E','L',"I"])
            if access == 'A':
                ShowInvent(database)
                save(database)
            elif access == 'B':
                addProduct(database)
                save(database)
            elif access == 'C':
                delProduct(database)
                save(database)
            elif access =='D':
                updProduct(database)
                save(database)
            elif access == 'E':
                cashier(database)
                save(database)
            elif access == 'L':
                loginput()
            elif access == 'I':
                information()
        def cashierdeny():
            clear_screen()
            print(f'''======= ACCESS DENIED =======
        
            Halo, {using.capitalize()} 
            Mohon maaf, untuk fitur ini hanya bisa
            diakses akun dengan status 'owner'.
            
            Apabila anda ingin menggunakan fitur ini
            silahkan menghubungi pemilik akun dengan
            status tersebut.
        
            Berikut adalah beberapa fitur yang bisa anda gunakan:
        
            A. Show Current Inventory Data
            E. Cashier Mode
        
            =======================
        
            L. Logout
            I. Information
        
            ''')
            access = pyip.inputChoice(
                prompt=("\nInput Option Code = \n"), 
                choices= ['A','E','L',"I","M"])
            if access == 'A':
                ShowInvent(database)
            elif access == 'E':
                cashier(database)
            elif access == 'L':
                loginput()
            elif access == 'I':
                information()
            elif access == 'M':
                MainMenu()   
        def menuCashier():
            clear_screen()
            print(header)
            access = pyip.inputChoice(
                    prompt=("\nInput Option Code = \n"), 
                    choices= ['A','B','C','D','E','L',"I"])
            if access == 'A':
                ShowInvent(database)
            elif access == 'B':
                clear_screen()
                cashierdeny()
            elif access == 'C':
                clear_screen()
                cashierdeny()
            elif access =='D':
                cashierdeny
            elif access == 'E':
                cashier(database)
            elif access == 'L':
                loginput()
            elif access == 'I':
                information()

        if posisi == 'owner':
            clear_screen()
            menuOwner()
        elif posisi == 'cashier':
            clear_screen()
            menuCashier()

# initiate program
def run(database):
    database = get_db()
    loginput()

    #write data
    with open(PATH, 'w') as file:
        PATH = r'C:\Users\attha\OneDrive\Documents\Dokumen Sementara (Nanti pindah hardisk)\Purwadhika JCDS-02\Capstone Projects\Module 1 - Programming\Reproject-Mode Malathi\data\data_prod.csv'
        dataWriter = csv.writer(file, delimiter=';', lineterminator='\n')
        dataWriter.writerows(database.values())

database = get_db()
run(database)
