# s3zilla
#### An S3 file-transfer client for Windows, developed in Python

<img src="<- TODO ->" alt="ex">
<hr>

<br><br>
See the <a href="https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html">documentation</a>
for setting up your S3 API keys, especially the
<i>Configuration Settings and Precedence</i> section.
<br><br>
I prefer using environment variables although you may
also use the credentials file as well.
<br><br>
This application assumes that at least one bucket has been
created in the AWS Console; it will list all available buckets
that are accessible with the S3 Access/Secret keys being used.
<br><br>
Neither one requires any changes in the code.
Simply set your API keys with your method of choice
and start using the program.
<br><br>
A trailing / after a name in the file explorer denotes a folder-object/directory.
<br><br>
The application assumes ACLs are disabled per each object in the contents of the bucket
and does not put private/public/readOnly ACLs on uploaded file-objects.
<br><br>
Multiple files can be selected at once for a single upload or download.
<br><br>
Requirements:
<code>pip install boto3</code>
<hr>
Tested on Windows 10/11
<b>Author: rootVIII  2019-2023</b>
