# MOLLECULES
class Molecule(object):
    
    def __init__(self, atomlist, left):
        self.atomlist = atomlist #a list of atom classes and/or molecule classes (for polyatomics)
        self.left = left #side of equation
        self.pos = atomlist[0].pos
        #self.numberlist=numberlist #number of each atom type
        #self.molenum=molenum
    #returns a string representation of the molecule in the format of Abbrev^NumAbbrev^Num

    def __str__(self):
        templist = []
        numlist = []
        for a in self.atomlist:
            if a.atomabbrev in templist:
                numlist[templist.index(a.atomabbrev)] += 1
            else:
                templist.append(a.atomabbrev)
                numlist.append(1)
        if (templist):
            rep = ''
            i = 0
            while i < len(templist):
                rep += (templist[i])
                rep += '^'
                rep += str(numlist[i])
                i += 1
            return rep

    def __lt__(self, other):
        self.atomlist.sort()
        other.atomlist.sort()
        if len(self.atomlist) < len(other.atomlist):
            return True
        elif len(self.atomlist) > len(other.atomlist):
            return False
        elif len(self.atomlist) == len(other.atomlist):
            i=0        
            while ((i < (len(self.atomlist))) and (i < (len(other.atomlist)))):
                if int(self.atomlist[i].atomnum) < int(other.atomlist[i].atomnum):
                    return True
                elif int(self.atomlist[i].atomnum) > int(other.atomlist[i].atomnum):
                    return False
                i += 1
            if ((i > len(self.atomlist)) and (i < len(other.atomlist))):
                return False
            elif ((i > len(other.atomlist)) and (i < len(self.atomlist))):
                return True
            else:
                return False

    def __cmp__(self, other):
        self.atomlist.sort()
        other.atomlist.sort()
        if len(self.atomlist) < len(other.atomlist):
            return -1
        elif len(self.atomlist) > len(other.atomlist):
            return 1
        elif len(self.atomlist) == len(other.atomlist):
            i=0        
            while ((i < (len(self.atomlist))) and (i < (len(other.atomlist)))):
                if int(self.atomlist[i].atomnum) < int(other.atomlist[i].atomnum):
                    return -1
                elif int(self.atomlist[i].atomnum) > int(other.atomlist[i].atomnum):
                    return 1
                i += 1
            if ((i > len(self.atomlist)) and (i < len(other.atomlist))):
                return 1
            elif ((i > len(other.atomlist)) and (i < len(self.atomlist))):
                return -1
            else:
                return 0

        
    def eqstr(self):
        numlist=[]
        templist=[]
        for a in self.atomlist:
            if a.atomabbrev in templist:
                numlist[templist.index(a.atomabbrev)]+=1
            else:
                templist.append(a.atomabbrev)
                numlist.append(1)
        rep=''
        i=0
        while i < len(templist):
            rep+=str(numlist[i])
            rep+=templist[i]
            i+=1
        return rep

    def update(self):
        count = 0
        newpos = None
        for a in self.atomlist:
            a.left = self.left
            a.update()
            if(count > 0):
                base = self.atomlist[0]
                if(count == 1):
                    newpos = (base.pos.x + (base.image_w), base.pos.y)
                elif(count == 2):
                    newpos = (base.pos.x, base.pos.y + (base.image_h))
                elif(count == 3):
                    newpos = (base.pos.x - (base.image_w), base.pos.y)
                elif(count == 4):
                    newpos = (base.pos.x, base.pos.y - (base.image_h))
                elif((count > 4) and (count < 8)):
                    base = self.atomlist[1]
                    if(count == 5):
                        newpos = (base.pos.x + (base.image_w), base.pos.y)
                    if(count == 6):
                        newpos = (base.pos.x, base.pos.y + (base.image_h))
                    if(count == 7):
                        newpos = (base.pos.x, base.pos.y - (base.image_h))
                elif((count > 7) and (count < 11)):
                    base = self.atomlist[3]
                    if(count == 8):
                        newpos = (base.pos.x - (base.image_w), base.pos.y)
                    if(count == 9):
                        newpos = (base.pos.x, base.pos.y + (base.image_h))
                    if(count == 10):
                        newpos = (base.pos.x, base.pos.y - (base.image_h))
                elif(count == 11):
                    base = self.atomlist[2]
                    newpos = (base.pos.x, base.pos.y + (base.image_h))
                elif(count == 12):
                    base = self.atomlist[4]
                    newpos = (base.pos.x, base.pos.y - (base.image_h))
                else:
                    odd = count%2
                    base = self.atomlist[count - 2]
                    if(odd == 1):
                        newpos = (base.pos.x, base.pos.y + (base.image_h))
                    else:
                        newpos = (base.pos.x, base.pos.y - (base.image_w))

                a.pos = newpos
                a.update()

            count += 1

        self.pos = self.atomlist[0].pos

    def blitme(self):
        for a in self.atomlist:
            a.update()
            a.blitme()
