# s3zilla
#### A cross-platform S3 file-transfer client, developed in Python

<img src="https://github.com/rootVIII/s3zilla/blob/master/sc.png" alt="ex" height="400" width="400">
<hr>

<pre>
  <code>
requirements:

python3

pip install boto3

Additional Linux Requirements: sudo apt-get install python3-tk
  </code>
</pre>
<br>

<pre>
  <code>
Download, navigate to project root, and run the following command
- ensure pip points to Python3 or use pip3 depending on your setup

pip install -e .

or install directly from Git:

pip install git+https://github.com/rootVIII/tube_dream

Then run the command from any location in your shell: s3zilla

Or run as a normal Python script: python s3zilla.py or python3 s3zilla.py
  </code>
</pre>
<br>
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

This was developed and tested on Ubuntu 18.04 and Kubuntu 18.04 (also tested on Windows 10).

<b>Author: James Loye Colley  2019-2020</b>
