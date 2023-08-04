lista1 = []
def imiona( file_name ):
    with open(f'{file_name}.txt','r') as imiona:
        for el in imiona:
            linia = imiona.readline()
            linia = linia.split()
            print( linia, end='' )
            if len(linia) > 0 :
                print( 'OK')
                lista1.append(linia[0])

    with open(f'imiona.txt','w') as imiona:
        for linia in lista1:
            linia = linia + '\n'
            imiona.write(linia)

imiona('meskie')
imiona('zenskie')