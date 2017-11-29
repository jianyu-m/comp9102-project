# Benchmark

## PowerGraph
** Important note: PowerGraph will download some dependencies while building, however, some of the URLs are broken. You need to fix them in CMakeLists.txt.**

### Step 0: Install GraphLab PowerGraph on one of your cluster nodes.

Install GraphLab PowerGraph, using instructions in the [README.md](README.md), on your master node (one of your cluster machines).

### Step 1: Copy GraphLab PowerGraph files to all machines.

1) Create a file called in your home directory called “machines” with the names of all the MPI nodes participate in the computation.

For example:

```
cat ~/machines
# hkucs-PowerEdge-R430-1
# hkucs-PowerEdge-R430-2
# ...
# hkucs-PowerEdge-R430-18
mynode1.some.random.domain
mynode2.some.random.domain
...
mynode18.some.random.domain
```
2) Verify you have the machines files from section 1) in your root folder of all of the machines.

3) You will need to setup password-less SSH between the master node and all other machines.

Verify it is possible to ssh without password between any pairs of machines. These [instructions](http://www.linuxproblem.org/art_9.html) explain how to setup ssh without passswords.

Before proceeding, verify that this is setup correctly; check that the following connects to the remote machine without prompting for a password:

```
# from machine mynode1.some.random.domain
# ssh hkucs-PowerEdge-R430-2
ssh mynode2.some.random.domain
```

4) On the node you installed GraphLab on, run the following commands to copy GraphLab files to the rest of the machines:

```
cd ~/graphlab/release/toolkits
~/graphlab/scripts/mpirsync
cd ~/graphlab/deps/local
~/graphlab/scripts/mpirsync
```

This step will only work if the file you created in step 1 was named "machines" and located in your home directory.

In order for mpirsync to run properly all machines must have all network ports open.

### Step 2a: Run PageRank on a synthetic graph

This step runs the [PageRank](http://en.wikipedia.org/wiki/PageRank) algorithm on a synthetic generated graph of 100,000 nodes. It spawns two GraphLab mpi instances (-n 2).
```
# ~/graphlab/release/toolkits/graph_analytics/pagerank
mpiexec -n 2 -hostfile ~/machines /path/to/pagerank --powerlaw=100000
```

## Giraph
** Important note: the default Hadoop version used by Giraph (1.3.0) is 1.2.1. For simplicity, please install Hadoop 1.2.1 instead of 0.20.203.0-RC1.**

### Deploying Hadoop
Create a dedicated `hadoop` group, a new user account `hduser`, and then add this user account to the newly created group:

```
sudo addgroup hadoop
sudo adduser --ingroup hadoop hduser
```
Next, download and extract `hadoop-0.20.203.0rc1` from Apache archives:
```
su - hdadmin
cd /usr/local
sudo wget http://archive.apache.org/dist/hadoop/core/hadoop-0.20.203.0/hadoop-0.20.203.0rc1.tar.gz
sudo tar xzf hadoop-0.20.203.0rc1.tar.gz
sudo mv hadoop-0.20.203.0 hadoop
sudo chown -R hduser:hadoop hadoop
```
After installation, swich to user account `hduser` and edit the account's `$HOME/.bashrc` with the following:

```
export HADOOP_HOME=/usr/local/hadoop
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
```

This will set Hadoop/Java related environment variables. After that, edit `$HADOOP_HOME/conf/hadoop-env.sh` with the following:

```
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
export HADOOP_OPTS=-Djava.net.preferIPv4Stack=true
```
The second line will force Hadoop to use IPv4 instead of IPv6, even if IPv6 is configured on the machine. As Hadoop stores temporary files during its computation, you need to create a base temporary directorty for local FS and HDFS files as follows:

```
su – hdadmin
sudo mkdir -p /app/hadoop/tmp
sudo chown hduser:hadoop /app/hadoop/tmp
sudo chmod 750 /app/hadoop/tmp
```

Now, edit Hadoop configuration files `core-site.xml`, `mapred-site.xml`, and `hdfs-site.xml` under `$HADOOP_HOME/conf` to reflect the current setup. Add the new lines between `<configuration>...</configuration>`, as specified below:

- Edit `core-site.xml` with:
  ```
  <property>
  <name>hadoop.tmp.dir</name>
  <value>/app/hadoop/tmp</value>
  </property>

  <property> 
  <name>fs.default.name</name> 
  <value>hdfs://hdnode01:54310</value> 
  </property>
  ```

- Edit `mapred-site.xml` with:
  ```
  <property>
  <name>mapred.job.tracker</name> 
  <value>hdnode01:54311</value>
  </property>

  <property>
  <name>mapred.tasktracker.map.tasks.maximum</name>
  <value>4</value>
  </property>

  <property>
  <name>mapred.map.tasks</name>
  <value>4</value>
  </property>
  ```

- Edit `hdfs-site.xml` with:
  ```
  <property>
  <name>dfs.replication</name>
  <value>1</value> 
  </property>
  ```

Next, set up SSH for user account `hduser` so that you do not have to enter a passcode every time an SSH connection is started:

```
su – hduser
ssh-keygen -t rsa -P ""
cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys
```
And then SSH to `hdnode01` under user account `hduser` (this must be to `hdnode01`, as we used the node's hostname in Hadoop configuration). You will be asked for a password if this is the first time you SSH to the node under this user account. When prompted, do store the public RSA key into `$HOME/.ssh/known_hosts`. Once you make sure you can SSH without a passcode/password, edit `$HADOOP_HOME/conf/masters` with this line:

```
hdnode01
```

Similarly, edit `$HADOOP_HOME/conf/slaves` with the following two lines:

```
hdnode01
```
These edits set a single-node, pseudo-distributed Hadoop cluster consisting of a single master and a single slave on the same physical machine. Note that if you want to deploy a multi-node, distributed Hadoop cluster, you should add other data nodes (e.g., `hdnode02`, `hdnode03`, ...) in the `$HADOOP_HOME/conf/slaves` file after following all of the steps above on each new node with minor changes. You can find more details on this at Apache Hadoop website.

Let us move on. To initialize HDFS, format it by running the following command:
```
$HADOOP_HOME/bin/hadoop namenode -format
```

And then start the HDFS and the map/reduce daemons in the following order:
```
$HADOOP_HOME/bin/start-dfs.sh
$HADOOP_HOME/bin/start-mapred.sh
```
Make sure that all necessary Java processes are running on both `hdnode01` by running this command:
```
jps
```
Which should output the following (ignore process IDs):
```
9079 NameNode
9560 JobTracker
9263 DataNode
9453 SecondaryNameNode
16316 Jps
9745 TaskTracker
```
To stop the daemons, run the equivelent `$HADOOP_HOME/bin/stop-*.sh` scripts in a reversed order. This is important so that you will not lose your date. You are done with deploying a single-node, pseudo-distributed Hadoop cluster.

### Deploying Giraph
We will now deploy Giraph. In order to build Giraph from the repository, you need first to install Git and Maven 3 by running the following commands:
```
su - hdadmin
sudo apt-get install git
sudo apt-get install maven
mvn -version
```
Make sure that you have installed Maven 3 or higher. Giraph uses the Munge plugin, which requires Mave 3, to support multiple versions of Hadoop. Also, the web site plugin requires Maven 3. You can now clone Giraph from its Github mirror:
```
cd /usr/local/
sudo git clone https://github.com/apache/giraph.git
sudo chown -R hduser:hadoop giraph
su - hduser
```
After that, edit `$HOME/.bashrc` for user account `hduser` with the following line:
```
export GIRAPH_HOME=/usr/local/giraph
```
Save and close the file, and then validate, compile, test (if required), and then package Giraph into JAR files by running the following commands:
```
source $HOME/.bashrc
cd $GIRAPH_HOME
mvn package -DskipTests
```
The argument `-DskipTests` will skip the testing phase. This may take a while on the first run because Maven is downloading the most recent artifacts (plugin JARs and other files) into your local repository. You may also need to execute the command a couple of times before it succeeds. This is because the remote server may time out before your downloads are complete. Once the packaging is successful, you will have the Giraph core JAR `$GIRAPH_HOME/giraph-core/target/giraph-1.2.0-SNAPSHOT-for-hadoop-0.20.203.0-jar-with-dependencies.jar` and Giraph examples JAR `$GIRAPH_HOME/giraph-examples/target/giraph-examples-1.1.0-SNAPSHOT-for-hadoop-0.20.203.0-jar-with-dependencies.jar`. You are done with deploying Giraph.
