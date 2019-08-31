# s3zilla
#### an S3 file-transfer client for Linux & Windows, developed in Python

<img src="https://github.com/rootVIII/s3zilla/blob/master/sc.png" alt="ex" height="800" width="950">
<hr>


<code>python s3zilla.py</code>

<code>./s3zilla.py</code>

<br>
<strong>Python3 is required</strong>


boto3 is also required:  <code>pip install boto3</code>

<br>
<strong>Additional Linux Requirements:</strong>

<code>sudo apt-get install python3-tk</code>

<code>sudo apt-get install libssl-dev</code>


See the <a href="https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html">documentation</a>
for setting up your S3 API keys, especially the
<i>Configuration Settings and Precedence</i> section.
<br><br>
I prefer using environment variables although you may
also use the credentials file as well.
<br><br>
Neither one requires any changes in the code.
Simply set your API keys with your method of choice
and start using the program.
<br><br>
If you attempt to upload a <b>directory</b> to a selected bucket, it will
be converted into a compressed .zip format prior to upload.
<br><br>
A trailing / after a name in the file explorer denotes a directory.
<br><br>
Multiple files can be selected at once for a single upload or download.
<hr>

This was developed and tested on Ubuntu 18.04. Also tested on Windows 10

<b>Author: James Loye Colley  2019</b>
