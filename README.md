# s3zilla
#### an S3 file-transfer client for Linux & Windows, developed in Python

<img src="https://github.com/rootVIII/s3zilla/blob/master/sc.png" alt="ex" height="800" width="950">
<hr>
<br>
<code>s3_zilla.py</code> -> Linux Version
<br>
<code> s3_zilla_WIND10.py</code>  -> Windows Version
<br><br>
<strong>Python3 is required</strong>
<br><br>
boto3 is also required:
<br>
<code>pip install boto3</code>
<br>
<br>
<strong>Additional Linux Requirements:</strong>:
<br> 
<code>sudo apt-get install python3-tk</code>
<br>
<code>sudo apt-get install libssl-dev</code>
<br>
<br>
<br>
Please see the 
<a href="https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html">
    documentation
</a>
for setting up your API keys, especially the <i>Configuration Settings and Precedence</i> section <br>
(I prefer environment variables).
<br><br>
If you attempt to upload a <b>directory</b> to a selected bucket, it will
be converted into a compressed .zip format prior to upload.
<br><br>
Multiple files can be selected at once for a single upload or download.
<br><br>
The code for the Windows version is exactly the same as the Linux version with the exception of some
placement/sizing of the Tkinter widgets.
<hr>
This was developed on Ubuntu 18.04
<br>
<b>Author: James Loye Colley  2019</b>
