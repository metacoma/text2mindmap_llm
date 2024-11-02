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
curl -sL https://github.com/metacoma/freeplane_plugin_grpc/releases/download/0.0.4/org.freeplane.plugin.grpc.tgz | tar zxvf - -C ~/freeplane/plugins/
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
. env
```
