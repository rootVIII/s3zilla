# s3zilla
#### an S3 file-transfer client for Linux & Windows, developed in Python

<img src="https://github.com/rootVIII/s3zilla/blob/master/sc.png" alt="ex" height="800" width="950">
<hr>
<strong>Requirements (Windows/Linux)</strong>:
<br>
<code>pip3 install boto3</code>
<br>
<br>
<strong>Linux</strong>: 
<code>sudo apt-get install python3-tk</code>
<br>
<code>sudo apt-get install libssl-dev</code>
<br>
<br>
Please follow these steps when initially setting up your s3zilla:
<br>
<ol>
  <li>
    Download your rootkey.csv from Amazon S3 (do not use the root user's keys)
  <li>
    Place the file into your home directory if on Linux.
  </li>
  <li>
    <strong>Or</strong> save <code>AWS_ACCESS_KEY_ID</code> and <code>AWS_SECRET_ACCESS_KEY</code> in
    your .bashrc or .bash_profile as environment variables.
  </li>
  <li>
    If using Windows, type "Environment Variables" into the search box and then save the environment variables
    with the same names shown above.
  </li>
</ol>
<br>
Since Amazon S3 is intended for files, if you attempt to upload a directory to a selected bucket, it will
be <strong>converted into a compressed .zip file prior to upload</strong>.
<br><br>
Multiple files can be selected at once for a single upload or download.
<br><br>
The code for the Windows version is exactly the same as the Linux version with the exception of some
placement/sizing of the Tkinter widgets.
<br>
<hr>
This was developed on Ubuntu 18.04
<hr>
<b>Author: James Loye Colley  2019</b>
