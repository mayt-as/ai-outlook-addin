import http.client
import mimetypes

def post_multipart(host, selector, fields, files):
    content_type, body = encode_multipart_formdata(fields, files)
    h = http.client.HTTPSConnection(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()

def encode_multipart_formdata(fields, files):
    LIMIT = '----------lImIt_of_THE_fIle_eW_$'
    CRLF = b'\r\n'
    L = []
    for (key, value) in fields:
        L.append(('--' + LIMIT).encode('utf-8'))
        L.append(('Content-Disposition: form-data; name="%s"' % key).encode('utf-8'))
        L.append(b'')
        L.append(value.encode('utf-8'))
    for (key, filename, value) in files:
        L.append(('--' + LIMIT).encode('utf-8'))
        L.append(('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename)).encode('utf-8'))
        L.append(('Content-Type: %s' % get_content_type(filename)).encode('utf-8'))
        L.append(b'')
        L.append(value)
    L.append(('--' + LIMIT + '--').encode('utf-8'))
    L.append(b'')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % LIMIT
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

with open('outlook_ai_addin.zip', 'rb') as f:
    import urllib.request
    try:
        req = urllib.request.Request("https://api.anonfiles.com/upload", data=encode_multipart_formdata([], [('file', 'outlook_ai_addin.zip', f.read())])[1], headers={'Content-Type': encode_multipart_formdata([], [('file', 'outlook_ai_addin.zip', b'dummy')])[0]})
        print(urllib.request.urlopen(req).read().decode('utf-8'))
    except Exception as e:
        print(e)
