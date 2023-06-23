using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;


namespace test
{
    public static class Program
    {
        public static directory currentdirectory;
        static string currentpath;
        public static class command
        {
            public static void cd()
            {
                Console.WriteLine("CD                Display the name or changes the current directory.");
            }
            public static void clr()
            {
                Console.WriteLine("CLR                Clears the screen.");
            }
            public static void dir1()
            {
                Console.WriteLine("DIR                Display a list of files and subdirectories.");
            }
            public static void help()
            {
                Console.WriteLine("HELP                Provide Help information for windows commands.");
            }
            public static void quit()
            {
                Console.WriteLine("QUIT                Quits the CMD.EXE Program(command interpreter).");
            }
            public static void copy()
            {
                Console.WriteLine("COPY                Copies one or more files to another location.");
            }
            public static void del()
            {
                Console.WriteLine("DEL                Deletes one or more files.");
            }
            public static void md()
            {
                Console.WriteLine("MD                Creates a directory.");
            }
            public static void md(string name22)
            {
                if (Program.currentdirectory.searchdirectory(name22) == -1)
                {
                    directoryentry d = new directoryentry(name22.ToCharArray(), 0x10, 0, 0);
                    Program.currentdirectory.directorytable.Add(d);
                    Program.currentdirectory.writedirectory();
                    if (Program.currentdirectory.parent1 != null)
                    {
                        Program.currentdirectory.parent1.updateContent(d);
                        Program.currentdirectory.writedirectory();
                    }
                }
                else
                {
                    Console.WriteLine($"A subdirectory or file {name22} already exists.");
                }
            }
            public static void rd(string name22)
            {
                int index = Program.currentdirectory.searchdirectory(name22);
                if (index != -1)
                {
                    int firstcluster = Program.currentdirectory.directorytable[index].first_cluster;
                    directory d = new directory(name22.ToCharArray(), 0x10, firstcluster, 0, Program.currentdirectory);
                    d.deletedirectory(name22);
                    d.writedirectory();
                    d.readdirectory();
                }
                else
                {
                    Console.WriteLine("The system cannot find the file specified.");
                }
            }
            public static void cd(string name22)
            {
                int index = Program.currentdirectory.searchdirectory(name22);
                if (index != -1)
                {
                    int firstcluster = currentdirectory.directorytable[index].first_cluster;
                    string path = Program.currentpath.Trim() + "\\" + name22;
                    // Console.WriteLine(path);
                    directory d = new directory(path.ToCharArray(), 0x10, firstcluster, 0, Program.currentdirectory);
                    currentdirectory = d;
                    currentdirectory.readdirectory();
                }
            }
            public static void rename(string name11, string name22)
            {
                int index = Program.currentdirectory.searchdirectory(name11);
                if (index != -1)
                {
                    int New = Program.currentdirectory.searchdirectory(name22);
                    if (New == -1)
                    {
                        directoryentry obj = Program.currentdirectory.directorytable[index];
                        obj.file_name = name22.ToCharArray();
                        Program.currentdirectory.directorytable.RemoveAt(index);
                        Program.currentdirectory.directorytable.Insert(index, obj);
                        Program.currentdirectory.writedirectory();
                    }
                    else
                    {
                        Console.WriteLine("this file is duplicated");
                    }
                }
                else
                {
                    Console.WriteLine("this file isnot exist");
                }
            }
            public static void export(string name, string path)
            {
                int s = Program.currentdirectory.searchdirectory(name);
                if (s != -1)
                {
                    if (System.IO.Directory.Exists(path))
                    {
                        int fc = Program.currentdirectory.directorytable[s].first_cluster;
                        int fs = Program.currentdirectory.directorytable[s].file_size;
                        string temp = "";
                        fileEntry f = new fileEntry(name.ToCharArray(), 0x0, fc, fs, Program.currentdirectory, temp);
                        f.writefile();
                        f.readfile();
                        StreamWriter streamWrite = new StreamWriter(path + "\\" + name);
                        streamWrite.Write(f.con_tent);
                        streamWrite.Flush();
                        streamWrite.Close();
                    }
                    else
                    {
                        Console.WriteLine("system can't find ");
                    }
                }
                else
                {
                    Console.WriteLine("can't find file");
                }
            }
            public static void import(string path)
            {
                if (File.Exists(path))
                {
                    string content = File.ReadAllText(path);
                    int size = content.Length;
                    int l = path.LastIndexOf("\\");
                    string n1 = path.Substring(l + 1);
                    int index = Program.currentdirectory.searchdirectory(n1);

                    if (index == -1)
                    {
                        int firstcluster;
                        if (size > 0)
                        {
                            firstcluster = fat.Getavaliableblock();
                        }
                        else
                        {
                            firstcluster = 0;
                        }
                        fileEntry f = new fileEntry(n1.ToCharArray(), 0x0, firstcluster, size, Program.currentdirectory, content);
                        f.writefile();
                        directory d = new directory(n1.ToCharArray(), 0x0, firstcluster, size, Program.currentdirectory);
                        Program.currentdirectory.directorytable.Add(d);
                        Program.currentdirectory.writedirectory();
                    }
                    else
                    {
                        Console.WriteLine("already exist");
                    }
                }
                else
                {
                    Console.WriteLine("this file isnot exist");
                }
            }
            public static void del(string name22)
            {
                int index = Program.currentdirectory.searchdirectory(name22);
                if (index != -1)
                {
                    int fileattribute = Program.currentdirectory.directorytable[index].file_attribute;
                    if (fileattribute == 0x0)
                    {
                        int firstcluster = Program.currentdirectory.directorytable[index].first_cluster;
                        int filesize = Program.currentdirectory.directorytable[index].file_size;
                        fileEntry inst = new fileEntry(name22.ToCharArray(), 0x0, firstcluster, filesize, Program.currentdirectory, null);
                        inst.deletefile(name22);
                    }
                    else
                    {
                        Console.WriteLine("the system cannot find the file secified");
                    }
                }
                else
                {
                    Console.WriteLine("the system cannot find the file secified");
                }
            }
            public static void type(string name22)
            {
                int index = Program.currentdirectory.searchdirectory(name22);
                if (index != -1)
                {
                    int firstcluster = Program.currentdirectory.directorytable[index].first_cluster;
                    int filesize = Program.currentdirectory.directorytable[index].file_size;
                    string content = null;
                    fileEntry inst = new fileEntry(name22.ToCharArray(), 0x0, firstcluster, filesize, Program.currentdirectory, content);
                    inst.readfile();
                    Console.WriteLine(inst.con_tent);
                }
                else
                {
                    Console.WriteLine("the system cannot find this file");
                }
            }
            public static void dir()
            {
                int filenumbercounter = 0;
                int dirnumbercounter = 0;
                int filesizecounter = 0;
                Console.Write(" directory of : ");
                Console.WriteLine(currentpath.Trim() + "\\");
                for (int i = 0; i < Program.currentdirectory.directorytable.Count; i++)
                {
                    if (Program.currentdirectory.directorytable[i].file_attribute == 0x0)
                    {
                        Console.WriteLine(Program.currentdirectory.directorytable[i].file_size + "    " + new string
                            (Program.currentdirectory.directorytable[i].file_name));
                        filenumbercounter++;
                        filesizecounter += Program.currentdirectory.directorytable[i].file_size;
                    }
                    else
                    {
                        Console.Write(" <DIR> " + "    ");
                        //Console.Write("     ");
                        Console.WriteLine(Program.currentdirectory.directorytable[i].file_name);
                        dirnumbercounter++;
                    }
                }
                Console.WriteLine(filenumbercounter + " file(s)     " + filesizecounter + " bytes ");
                Console.WriteLine(dirnumbercounter + " Dir(s)     " + fat.getfreespace() + "   bytes free");
            }
            public static void copy(string source, string destination)
            {
                int index = Program.currentdirectory.searchdirectory(source);
                if (index != -1)
                {
                    int l = destination.LastIndexOf("\\");
                    string variable = destination.Substring(l + 1);
                    int index2 = Program.currentdirectory.searchdirectory(variable);
                    if (destination != Program.currentdirectory.file_name.ToString())
                    {
                        int firstcluster = Program.currentdirectory.directorytable[index].first_cluster;
                        int filesize = Program.currentdirectory.directorytable[index].file_size;
                        directoryentry obj = new directoryentry(source.ToCharArray(), 0x0, firstcluster, filesize);
                        directory dir = new directory(variable.ToCharArray(), 0x10, firstcluster, filesize, Program.currentdirectory.parent1);
                        dir.directorytable.Add(obj);

                        dir.writedirectory();
                        Program.currentdirectory.directorytable.RemoveAt(index2);
                        Program.currentdirectory.directorytable.Add(dir);
                        Program.currentdirectory.writedirectory();
                        //dir.readdirectory();
                    }
                    else
                    {
                        Console.WriteLine("cannot find file path");
                    }
                }
            }
            public static void rd()
            {
                Console.WriteLine("RD                Removes a directory.");
            }

            public static void rename()
            {
                Console.WriteLine("RENAME                Renames a file or files.");
            }
            public static void type()
            {
                Console.WriteLine("TYPE                Ddisplay the contents of a text file.");
            }
        }
        static FileStream f1; //the name of the file.

        //class that reserve the places with any data cuz when i want write in it would override.  
        // make the file of abc (our virtual disk)
        static public class virtualdisk
        {
            public static directory root; //object from class directory 
            static public void initialize() //function that write in the virtual disk
            {
                byte b1 = (byte)'0'; // super block
                byte b2 = (byte)'*'; // fat table 
                byte b3 = (byte)'#'; //data file
                string fileabc = "E:\\abc.txt";


                if (!File.Exists(fileabc))
                {
                    f1 = new FileStream("E:\\abc.txt", FileMode.Create, FileAccess.Write);
                    for (int i = 0; i < 1048576; i++)
                    {

                        if (i >= 0 && i < 1024)  // (reserved for card information ) first 1024 byte
                        {
                            f1.WriteByte((byte)b1);
                        }
                        else if (i >= 1024 && i < 4096) // 1024*4
                        {
                            f1.WriteByte((byte)b2);
                        }
                        else
                        {
                            f1.WriteByte((byte)b3); //1019*1024
                        }
                    }
                    // reserve with -1 
                    fat.initialize();
                    directory root = new directory("H:".ToCharArray(), 0x10, 5, 0, null);
                    f1.Close();
                    root.writedirectory();
                    Program.currentdirectory = root;
                    fat.writefattable();
                }
                else

                {
                    fat.getfattable();
                    directory root = new directory("H:".ToCharArray(), 0x10, 5, 0, null);
                    root.readdirectory();
                    //make the parent as rooot 
                    Program.currentdirectory = root;
                }
            }


            static public void writeblock(byte[] w, int ind)
            {
                f1 = new FileStream("E:\\abc.txt", FileMode.Open, FileAccess.Write);
                f1.Seek(ind * 1024, SeekOrigin.Begin);
                f1.Write(w, 0, w.Length);
                f1.Close();
            }
            static public byte[] getblock(int ind)
            {
                f1 = new FileStream("E:\\abc.txt", FileMode.Open, FileAccess.Read);
                f1.Seek(ind * 1024, SeekOrigin.Begin);
                byte[] b = new byte[1024];
                f1.Read(b, 0, b.Length);
                f1.Close();
                return b;
            }
        }
        // (2-5) blocks it fill the fat table with any data 
        static public class fat
        {
            public static int[] fattable;
            public static int index;
            static byte[] b = new byte[4096];

            static public void initialize() //function that write in the fat table 
            {
                fattable = new int[1024];
                //this for loop fill the other 4 blocks with (-1) to reserve it with -1 to prevent writing on it
                for (int i = 0; i < fattable.Length; i++)
                {
                    if (i < 5)
                    {
                        fattable[i] = -1;
                    }
                }
            }
            static public void writefattable() // function that write in fat table 

            {  // 
                f1 = new FileStream("E:\\abc.txt", FileMode.Open, FileAccess.Write);
                // skip the first 1024 byte 
                f1.Seek(1024, SeekOrigin.Begin);
                // covert from integer to byte 
                Buffer.BlockCopy(fattable, 0, b, 0, 4096);
                f1.Write(b, 0, b.Length);
                f1.Close();
            }
            static public void getfattable()// read fattable
            {
                fat.initialize();
                f1 = new FileStream("E:\\abc.txt", FileMode.Open, FileAccess.Read);
                f1.Seek(1024, SeekOrigin.Begin);
                f1.Read(b, 0, b.Length);
                Buffer.BlockCopy(b, 0, fattable, 0, 4096);
                f1.Close();
            }

            static public void printfattable()
            {
                for (int i = 0; i < 1024; i++)
                {
                    Console.Write(i);
                    Console.Write(" ");
                }
            }
            // return the first empty block 
            static public int Getavaliableblock()
            {
                for (int i = 0; i < 1024; i++)
                {
                    if (fattable[i] == 0)
                    {
                        return (i);
                    }
                }
                return -1;
            }
            //return the value of index 
            static public int getnext(int ind)
            {
                return (fattable[ind]);
            }
            // take an index and value 
            static public void setnext(int index, int value)
            {
                fattable[index] = value;
            }
            //return the number of empty blocks 
            static public int getavailableblocks()
            {
                int counter = 0;
                for (int i = 0; i < fattable.Length; i++)
                {
                    if (fattable[i] == 0)
                    {
                        counter++;
                    }
                }
                return counter;
            }
            //return freespaces after we make files and directories 
            static public int getfreespace()
            {
                return getavailableblocks() * 1024;
            }
        }
        public class directoryentry
        {
            public char[] file_name = new char[11]; //file name stored in 11 charcter
            public byte[] file_empty = new byte[12];       //zeros
            public byte file_attribute;   // 0x0 or 0x10
            public int file_size;
            public int first_cluster; //begining with root
            public byte[] tobyte = new byte[32];
            public directoryentry() { }
            public directoryentry(char[] filename, byte fileattribute, int firstcluster, int filesize)
            {
                //the filename should be 11 char if <11...spaces 
                string s = new string(filename);
                if (filename.Length < 11)
                {
                    for (int i = filename.Length; i < 11; i++)
                    {
                        s += " ";
                    }

                }

                file_name = s.ToCharArray();
                file_attribute = fileattribute;
                first_cluster = firstcluster;
                file_size = filesize;
            }
            // store the main information (4) in array of bytes 
            //return array overall 
            public byte[] getbyte()
            {
                //Convert array of char (file name) to array of bytes 
                byte[] ss = Encoding.ASCII.GetBytes(file_name);
                for (int i = 0; i < 11; i++)
                {
                    if (i < ss.Length)
                        tobyte[i] = ss[i];
                    else
                        tobyte[i] = (byte)' ';
                }

                tobyte[11] = file_attribute; // atribute stores in one byte (index 11)

                //file empty
                for (int i = 12; i < 24; i++)
                {
                    tobyte[i] = 0;
                }
                // Convert one int to array of bytes 
                byte[] tobyte2 = BitConverter.GetBytes(first_cluster);
                for (int i = 24, c = 0; i < 28; i++, c++)
                {
                    tobyte[i] = tobyte2[c];
                }
                //one integer will stored in 4 bytes
                byte[] tobyte3 = BitConverter.GetBytes(file_size);
                for (int i = 28, c = 0; i < 32; i++, c++)
                {
                    tobyte[i] = tobyte3[c];
                }
                return tobyte;
            }
            //function return array record by record 
            public directoryentry getdirectoryentry(byte[] arrb)
            {
                directoryentry d = new directoryentry();
                for (int i = 0; i < 11; i++)
                {
                    d.file_name[i] = (char)arrb[i];
                }

                d.file_attribute = arrb[11];
                //file empty 
                for (int i = 0; i < 12; i++)
                {
                    d.file_empty[i] = 0;
                }
                //first cluster
                byte[] fc = new byte[4];
                for (int i = 24; i < 28; i++)
                {
                    fc[i - 24] = arrb[i];
                }
                //after he store it as bytes it convert it to intger
                d.first_cluster = BitConverter.ToInt32(fc, 0);

                //file size 
                byte[] fs = new byte[4];
                for (int i = 28; i < 32; i++)
                {
                    fs[i - 28] = arrb[i];
                }
                d.file_size = BitConverter.ToInt32(fs, 0);
                return d;
            }
        }
        // list of directoryenteries
        public class directory : directoryentry
        {
            public List<directoryentry> directorytable = new List<directoryentry>();
            public directory parent1;
            public directory(char[] filen, byte fileatt, int firstclu, int filesi, directory parent1) : base(filen, fileatt, firstclu, filesi)
            {
                directorytable = new List<directoryentry>();
                if (parent1 != null)
                {
                    this.parent1 = parent1;
                }
            }
            public void writedirectory()
            {
                byte[] Directory_table_bytes = new byte[directorytable.Count * 32];//all table  
                byte[] Directory_Entry_bytes = new byte[32]; //array of bytes(entry)
                for (int i = 0; i < directorytable.Count; i++)//directorytable store as a byte 
                {
                    Directory_Entry_bytes = directorytable[i].getbyte();
                    for (int j = i * 32; j < ((i + 1) * 32); j++)
                    {
                        Directory_table_bytes[j] = Directory_Entry_bytes[j % 32];
                    }
                }
                double number_of_required_blocks = Math.Ceiling(Directory_table_bytes.Length / 1024.0);//number of blocks 
                int number_of_full_size_block = Directory_table_bytes.Length / 1024;//number of blocks without rem
                int reminder = Directory_table_bytes.Length % 1024;//number of byte
                if (number_of_required_blocks <= fat.getavailableblocks())//number of available block 
                {
                    List<byte[]> ls = new List<byte[]>();
                    if (Directory_table_bytes.Length > 0)
                    {
                        byte[] b = new byte[1024];
                        for (int i = 0; i < number_of_full_size_block; i++)
                        {
                            for (int j = i * 1024; j < ((i + 1) * 1024); j++)
                                b[j % 1024] = Directory_table_bytes[j];
                            ls.Add(b);
                        }
                        if (reminder > 0)//number of rem bytes
                        {
                            b = new byte[1024];
                            for (int i = number_of_full_size_block * 1024, k = 0; k < reminder; i++, k++)
                            {
                                b[k] = Directory_table_bytes[i];
                            }
                            ls.Add(b);
                        }
                    }
                    else
                    {
                    }

                    int FI;
                    int LFI = -1;
                    if (this.first_cluster != 0)//specify place 
                    {
                        FI = this.first_cluster;
                    }
                    else
                    {
                        FI = fat.Getavaliableblock();//return avaliableblock
                        this.first_cluster = FI;
                    }
                    for (int i = 0; i < number_of_required_blocks; i++)

                    {
                        virtualdisk.writeblock(ls[i], FI);//block and index
                        fat.setnext(FI, -1);//reserved 
                        if (LFI != -1)//empty 
                            fat.setnext(LFI, FI);
                        LFI = FI;
                        FI = fat.Getavaliableblock();
                    }
                    if (directorytable.Count == 0)
                    {
                        if (first_cluster != 0)
                        {
                            fat.setnext(first_cluster, 0);
                            first_cluster = 0;

                        }
                    }
                    fat.writefattable();
                }
                else { Console.WriteLine("directory size  exceeds free space size "); }
            }
            public int searchdirectory(string name)
            {
                string s;
                readdirectory();
                if (name.Length < 11)
                {
                    for (int i = name.Length; i < 11; i++)
                    {
                        name += " ";
                    }
                }
                for (int i = 0; i < directorytable.Count; i++)
                {
                    s = new string(directorytable[i].file_name);
                    if (string.Equals(s.Replace("\0", " ").Trim(), name.Trim()))
                    {
                        return i;
                    }
                }
                return -1;
            }
            public void readdirectory()
            {
                directorytable = new List<directoryentry>();

                int next = 0;
                int fatindex1;

                if (this.first_cluster != 0 && fat.getnext(first_cluster) != 0)
                {
                    fatindex1 = this.first_cluster;

                    next = fat.getnext(fatindex1);
                    List<byte> ls = new List<byte>();
                    do
                    {
                        ls.AddRange(virtualdisk.getblock(fatindex1));
                        fatindex1 = next;
                        if (fatindex1 != -1)
                            next = fat.getnext(fatindex1);

                    } while (fatindex1 != -1);
                    byte[] copy = new byte[32];

                    for (int i = 0; i < ls.Count; i++)
                    {
                        copy[i % 32] = ls[i];
                        if ((i + 1) % 32 == 0)
                        {
                            directoryentry d = getdirectoryentry(copy);
                            if (d.file_name[0] != '\0')
                                directorytable.Add(d);
                        }
                    }
                }

            }
            public void updateContent(directoryentry d)
            {
                int index = 0;
                readdirectory();
                index = searchdirectory(d.file_name.ToString());
                if (index != -1)
                {
                    directorytable.RemoveAt(index);
                    directorytable.Insert(index, d);
                }
                writedirectory();
            }
            public void deletedirectory(string g)
            {
                int next;
                int index = 0;
                //if it filled
                if (first_cluster != 0)
                {
                    index = first_cluster;
                    next = fat.getnext(index);
                    do
                    {
                        fat.setnext(index, 0);
                        index = next;
                        if (index != -1)
                        {
                            next = fat.getnext(index);
                        }
                    }
                    while (index != -1);
                }
                if (parent1 != null)
                {
                    parent1.readdirectory();
                    index = parent1.searchdirectory(g);
                    if (index != -1)
                    {
                        parent1.directorytable.RemoveAt(index);
                        parent1.writedirectory();
                    }
                }
                fat.writefattable();
            }
        }
        public class fileEntry : directoryentry
        {
            public directory parent1;
            public string con_tent = null;
            public fileEntry() { }
            public fileEntry(char[] filename, byte fileattribute, int firstcluster, int filesize, directory parent1, string content) : base(filename, fileattribute, firstcluster, filesize)
            {
                con_tent = content;
                if (parent1 != null)
                {
                    this.parent1 = parent1;
                }
            }
            public void writefile()
            {
                int fatindex, last_index = -1;
                byte[] by = Encoding.ASCII.GetBytes(con_tent);
                double numofreqblocks = Math.Ceiling(by.Length / 1024.0);
                int allsize = (by.Length / 1024);
                int rem = (by.Length % 1204);
                if (numofreqblocks <= fat.getavailableblocks())
                {
                    if (this.first_cluster != 0)
                    {
                        fatindex = this.first_cluster;
                    }

                    else
                    {
                        fatindex = fat.Getavaliableblock();
                        this.first_cluster = fatindex;
                    }
                    List<byte[]> blocks = new List<byte[]>();
                    byte[] block = new byte[1024];
                    for (int i = 0; i < allsize; i++)
                    {
                        for (int j = i * 1204, c = 0; c < 1024; c++, i++)
                        {
                            block[c] = by[i];
                        }
                        blocks.Add(by);
                    }
                    if (rem > 0)
                    {
                        block = new byte[1024];
                        int start = allsize * 1024;
                        for (int i = 0; i < (start + rem); i++)
                        {
                            block[i % 1024] = by[i];
                        }
                        blocks.Add(block);
                    }
                    for (int i = 0; i < blocks.Count; i++)
                    {
                        virtualdisk.writeblock(blocks[i], fatindex);
                        fat.setnext(fatindex, -1);
                        if (last_index != -1)
                        {
                            fat.setnext(last_index, fatindex);
                        }
                        else
                        {
                            last_index = fatindex;
                            fatindex = fat.getavailableblocks();
                        }
                    }
                }
                fat.writefattable();
            }
            public void readfile()
            {
                if (this.first_cluster != 0)
                {
                    con_tent = string.Empty;
                    int fatindex1 = this.first_cluster;
                    int next = fat.getnext(fatindex1);
                    List<byte> ls = new List<byte>();
                    //    fat.getnext(fatindex1);
                    do
                    {
                        ls.AddRange(virtualdisk.getblock(fatindex1));
                        fatindex1 = next;
                        if (fatindex1 != -1)
                            next = fat.getnext(fatindex1);

                    } while (next != -1);
                    string str = string.Empty;
                    for (int i = 0; i < ls.Count; i++)
                    {
                        if (Convert.ToChar(ls[i]) != '\0')
                        {
                            str += Convert.ToChar(ls[i]);
                        }
                    }
                    con_tent = str;
                }
            }
            public void deletefile(string g)
            {
                int next;
                int index;
                if (first_cluster != 0)
                {
                    index = first_cluster;
                    next = fat.getnext(index);
                    do
                    {
                        fat.setnext(index, 0);
                        index = next;
                        if (index != -1)
                        {
                            next = fat.getnext(index);
                        }
                    }
                    while (index != -1);
                }
                if (parent1 != null)
                {
                    parent1.readdirectory();
                    index = parent1.searchdirectory(g);
                    if (index != -1)
                    {
                        parent1.directorytable.RemoveAt(index);
                        parent1.writedirectory();
                    }
                }
                fat.writefattable();
            }
            static void Main(string[] args)
            {
                virtualdisk.initialize();


                string input;
                do
                {
                    currentpath = new string(currentdirectory.file_name); //H //root
                    string dir = currentpath;
                    Console.Write(dir.Trim() + "> ");
                    input = Console.ReadLine();
                    input = input.ToLower();
                    string[] in1 = input.Split(' ');// once it find space make split
                    if (in1[0] == "help" && in1.Length > 1)
                    {
                        if (in1[1] == "cd")
                        {
                            command.cd();
                        }
                        else if (in1[1] == "clr")
                        {
                            command.clr();
                        }
                        else if (in1[1] == "dir")
                        {
                            command.dir1();
                        }
                        else if (in1[1] == "help")
                        {
                            command.help();
                        }
                        else if (in1[1] == "quit")
                        {
                            command.quit();
                        }
                        else if (in1[1] == "copy")
                        {
                            command.copy();
                        }
                        else if (in1[1] == "del")
                        {
                            command.del();
                        }
                        else if (in1[1] == "md")
                        {
                            command.md();
                        }
                        else if (in1[1] == "rd")
                        {
                            command.rd();
                        }
                        else if (in1[1] == "rename")
                        {
                            command.rename();
                        }
                        else if (in1[1] == "type")
                        {
                            command.type();
                        }
                        else
                        {
                            Console.WriteLine("not recognized as an internal or external command");
                        }
                    }
                    else if (input == "help")
                    {
                        command.cd();
                        command.clr();
                        command.dir1();
                        command.md();
                        command.copy();
                        command.rename();
                        command.del();
                        command.md();
                        command.rd();
                        command.rename();
                        command.type();
                    }
                    else if (input == "cls")
                    {
                        Console.Clear();
                    }
                    else if (input == "exit")
                    {
                        Environment.Exit(0);
                    }
                    else if (input == "dir")
                    {
                        command.dir();
                    }
                    else if (in1.Length > 1)
                    {
                        if (in1[0] == "md")
                        {
                            command.md(in1[1]);
                        }
                        else if (in1[0] == "rd")
                        {
                            command.rd(in1[1]);
                        }
                        else if (in1[0] == "cd")
                        {
                            command.cd(in1[1]);
                        }
                        else if (in1[0] == "rename")
                        {
                            command.rename(in1[1], in1[2]);
                        }
                        else if (in1[0] == "type")
                        {
                            command.type(in1[1]);
                        }
                        else if (in1[0] == "del")
                        {
                            command.del(in1[1]);
                        }
                        else if (in1[0] == "import")
                        {
                            command.import(in1[1]);
                        }
                        else if (in1[0] == "export")
                        {
                            command.export(in1[1], in1[2]);
                        }
                        else if (in1[0] == "copy")
                        {
                            command.copy(in1[1], in1[2]);
                        }
                    }
                    else
                    {
                        Console.WriteLine("not recognized as an internal or external command");
                    }
                } while (input != "exit");
            }
        }
    }
}