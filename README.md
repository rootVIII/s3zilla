# s3zilla
#### An S3 file-transfer client for Windows, developed in Python

<img src="https://user-images.githubusercontent.com/30498791/230790628-2eca6bb0-83b0-4388-a067-b8551e9427af.gif" alt="ex">
<hr>

<br><br>
See the <a href="https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html">documentation</a>
for setting up your S3 API keys, especially the
<i>Configuration Settings and Precedence</i> section.
Typically use environment variables or the AWS credentials file.
Neither requires any changes in the code.
Simply set your API keys with your method of choice
and start using the program.
<br><br>
This application assumes that at least one bucket has been
created in the AWS Console; it will list all available buckets
that are accessible with the S3 Access/Secret keys being used.
<br><br>
A trailing / after a name in the file explorer denotes a directory.
A local directory may only be uploaded to S3 using s3zilla if it
contains at least one file. S3 itself doesn't really have a concept
of folders, but s3zilla directory uploads will follow the same
structure as the given folder being uploaded. Therefor directories
found in an S3 bucket that are visible within s3zill are not actually
be directories; they are a representation of directories that are
actually S3 file objects. For example, if a directory is uploaded to
S3 from your local machine with the name test/ and contains two files
named test1.pdf and test2.docx, they will appear as test/test1.pdf
and test/test2.docx in S3.
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
