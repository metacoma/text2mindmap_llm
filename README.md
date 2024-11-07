OSX:

  0. Install requirements: 
     ```
     brew install openjdk@17 git python3
     sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk
     echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
     ```  
  1. Install freeplane from dmg file:
     
     apple https://sourceforge.net/projects/freeplane/files/freeplane%20stable/archive/1.10.6/Freeplane-1.10.6-apple.dmg/download

     intel https://sourceforge.net/projects/freeplane/files/freeplane%20stable/archive/1.10.6/Freeplane-1.10.6-intel.dmg/download

  3. Install plugin
     Before install plugin, enable access to the plugin folder:

         open Settings -> Privacy & Security -> App management -> iTerm allow to update other application

     
     ```
     cd /Applications/Freeplane.app/Contents/app/plugins
     sudo curl -sL https://github.com/metacoma/freeplane_plugin_grpc/releases/download/0.0.5/org.freeplane.plugin.grpc.tgz | tar zxvf - -C .
     ```
   5. Install text2mindmap_llm
      ```
      git clone https://github.com/metacoma/text2mindmap_llm
      cd text2mindmap_llm
      echo export OPENAI_API_KEY="XXX" > .env
      . ./.env
      python3 -m venv .venv
      . .venv/bin/activate
      pip3 install -r requirements.txt
      ```
   6. Test
      ```
      ls | python3 ./text2mindmap.py
      ```
   7. Create keyboard shortcut to call workflow:
      ```
      Shortcuts -> New -> Run shell script
      ```
      ![image](https://github.com/user-attachments/assets/203e2867-8b60-4e45-b0b8-92650ed98991)
      ![image](https://github.com/user-attachments/assets/6248cec8-a814-4d59-b3e2-570270baa6b4)
      ```
      Keyboard -> Keyboard Shortcuts -> Services -> Shortcuts
      ```
      ![image](https://github.com/user-attachments/assets/914ea767-fa84-49ce-b17e-242ed871423b)


  
Step-by-step for most common Linux and BSD system:
1. Install freeplane 1.10.6
```
curl -o /tmp/freeplane.zip -L https://sourceforge.net/projects/freeplane/files/freeplane%20stable/archive/1.10.6/freeplane_bin-1.10.6.zip/download
unzip /tmp/freeplane.zip -d /tmp 
mv /tmp/freeplane-1.10.6/ ~/freeplane/
```

2. Install freeplane grpc plugin
Find the directory where freeplane stores plugin files (usually it is /usr/share/freeplane/plugins)
```
curl -sL https://github.com/metacoma/freeplane_plugin_grpc/releases/download/0.0.5/org.freeplane.plugin.grpc.tgz | tar zxvf - -C ~/freeplane/plugins/
```
3. Start freeplane
```
~/freeplane/freeplane.sh
```
4. Check that freeplane is listen 50051 tcp port on the 127.0.0.1 for the grpc requsts
```
$ netstat -nlp 2>/dev/null| grep 50051
tcp6       0      0 :::50051                :::*                    LISTEN      8289/java
```
5. Install python3 and python3 virtualenv package
6. 
```
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```
7. Set your openapi token
```
echo export OPENAI_API_KEY="XXX" > .env
. ./.env
```
