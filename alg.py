import numpy as np
import matplotlib.pyplot as plt
from PIL import Image




def encrypt():
    try:
        c1=np.load("static/c1.npy")
        c2=np.load('static/c2.npy')
        c3=np.load('static/c3.npy')
        d1=np.load('static/d1.npy')
        d2=np.load('static/d2.npy')
        d3=np.load('static/d3.npy')
        img=plt.imread('static/img.tiff')
        
        r=256*256*3
        img=np.array(img,dtype=np.uint8)
        
        do = Image.open('static/img.tiff')
        do.save('static/do.png')



        img=img.reshape(r,)
        msb=[]
        lsb=[]

        #seperating LSB and MSB from each pixel of image

        for i in range(0,len(img)):
            a=img[i]
            a=bin(a)
            a=a.replace('0b','')
            a=str(int(a)+100000000)
            msb.append(a[1:5])
            lsb.append(a[5:9])
        for i in range(0,len(c1)):
            msb[i]=int(msb[i],2)


        #confussion
        #1
        com=[]
        for i in range(0,len(c1)):
            com.append([c1[i], msb[i]])

        com=sorted(com)
        e_c1=[]
        for i in range(0,len(c1)):
            e_c1.append(com[i][1])

        #2
        com=[]
        for i in range(0,len(c2)):
            com.append([c2[i], e_c1[i]])

        com=sorted(com)
        e_c2=[]
        for i in range(0,len(c2)):
            e_c2.append(com[i][1])
        #3
        com=[]
        for i in range(0,len(c3)):
            com.append([c3[i], e_c2[i]])

        com=sorted(com)
        e_c3=[]
        for i in range(0,len(c2)):
            e_c3.append(com[i][1])



        #diffusion

        e_d1=[]
        e_d2=[]
        e_d3=[]
        for i in range(0,len(d1)):
            e_d1.append(int(e_c3[i])^int(d1[i]))
            e_d2.append(int(e_d1[i])^int(d2[i]))
            e_d3.append(int(e_d2[i])^int(d3[i]))
        e_i=[]
        cc=[]
        for i in range(0,len(c1)):
            a=e_d3[i]
            a=bin(a)
            a=a.replace('0b','')
            a=str(int(a)+10000)
            a=a[1:5]
            cc.append(a)
        for i in range(0,len(c1)):
            e_i.append(int(cc[i]+lsb[i],2))    
        e_i=np.array(e_i,dtype=np.uint8)
        e_i=e_i.reshape(256,256,3)
        enc= Image.fromarray(e_i)
        enc.save('static\enimg.tiff')

        de = Image.open('static\enimg.tiff')
        de.save('static\de.png')
    except:return None


def decrypt():
    print('decryption')
    try:
        c1=np.load('static\c1.npy')
        c2=np.load('static\c2.npy')
        c3=np.load('static\c3.npy')
        d1=np.load('static\d1.npy')
        d2=np.load('static\d2.npy')
        d3=np.load('static\d3.npy')
        img=plt.imread('static\enimg.tiff')


        de = Image.open('static\enimg.tiff')
        de.save('static\de.png')


        r=256*256*3
        img=np.array(img,dtype=np.uint8)
        img=img.reshape(r,)

        msb=[]
        lsb=[]

        #seperating LSB and MSB from each pixel of image

        for i in range(0,len(img)):
            a=img[i]
            a=bin(a)
            a=a.replace('0b','')
            a=str(int(a)+100000000)
            msb.append(a[1:5])
            lsb.append(a[5:9])
        for i in range(0,len(c1)):
            msb[i]=int(msb[i],2)
        

        #diffusion

        e_d1=[]
        e_d2=[]
        e_d3=[]
        for i in range(0,len(d1)):
            e_d3.append(int(msb[i])^int(d3[i]))
            e_d2.append(int(e_d3[i])^int(d2[i]))
            e_d1.append(int(e_d2[i])^int(d1[i]))

            
        #confussion
        #1
        ind=[]
        for i in range(0,len(c3)):
            ind.append(i)
        com=[]
        k22=[]
        for i in range(0,len(c3)):
            com.append([c3[i], ind[i]])

        com=sorted(com)
        index_key=[]
        for i in range(0,len(ind)):
            index_key.append(com[i][1])
        com=[]
        for i in range(0,len(index_key)):
            com.append([index_key[i], e_d1[i]])

        com=sorted(com)

        d_c3=[]
        for i in range(0,len(index_key)):
            d_c3.append(com[i][1])
            
            
        #2 
            
        ind=[]
        for i in range(0,len(c2)):
            ind.append(i)
        com=[]
        k22=[]
        for i in range(0,len(c2)):
            com.append([c2[i], ind[i]])

        com=sorted(com)
        index_key=[]
        for i in range(0,len(ind)):
            index_key.append(com[i][1])
        com=[]
        for i in range(0,len(index_key)):
            com.append([index_key[i], d_c3[i]])

        com=sorted(com)

        d_c2=[]
        for i in range(0,len(index_key)):
            d_c2.append(com[i][1])
            
        #3 
        ind=[]
        for i in range(0,len(c1)):
            ind.append(i)
        com=[]
        k22=[]
        for i in range(0,len(c1)):
            com.append([c1[i], ind[i]])

        com=sorted(com)
        index_key=[]
        for i in range(0,len(ind)):
            index_key.append(com[i][1])
        com=[]
        for i in range(0,len(index_key)):
            com.append([index_key[i], d_c2[i]])

        com=sorted(com)

        d_c1=[]
        for i in range(0,len(index_key)):
            d_c1.append(com[i][1])
    
                
        e_i=[]
        cc=[]
        for i in range(0,len(d_c1)):
            a=d_c1[i]
            a=bin(a)
            a=a.replace('0b','')
            a=str(int(a)+10000)
            a=a[1:5]
            cc.append(a)
        for i in range(0,len(c1)):
            e_i.append(int(cc[i]+lsb[i],2))    
        e_i=np.array(e_i)
        print(e_i)
        e_i=e_i.reshape(256,256,3)
        e_i=np.array(e_i,dtype=np.uint8)
        enc= Image.fromarray(e_i)
        enc.save('static\deimg.tiff')

        dd = Image.open('static\deimg.tiff')
        dd.save('static\dd.png')
    except:return None
