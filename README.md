# s3zilla
#### an S3 file-transfer client for Linux & Windows, developed in Python

<img src="https://github.com/rootVIII/s3_zilla/blob/master/sc.png" alt="ex" height="800" width="950">
<hr>
Requirements:
<br>
<code>pip3 install boto3</code>
<br>
<br>
<strong>Linux: 
<code>sudo apt-get install python3-tk</code>
<br>
<code>sudo apt-get install libssl-dev</code>
<br>
<br>
s3zilla uses an encrypted version of your rootkey.csv file.
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
    Or save <code>AWS_ACCESS_KEY_ID</code> and <code>AWS_SECRET_ACCESS_KEY</code> in your .bashrc or .bash_profile.
  </li>
  <li>
    Windows: In search box type "Environment Variables" - save the environment variables as shown above.
  </li>
</ol>
<br>
<br>
Since Amazon S3 is intended for files, if you attempt to upload a directory to a selected bucket, it will
be <strong>converted into a compressed .zip file prior to upload</strong>.
<br>
<hr>
This was developed on Ubuntu 18.04
<hr>
<b>Author: James Loye Colley  2019</b>
