import qrcode
from django.conf import settings


def generate_qrcode(nid):
    '''
    生成二维码
    :param request:
    :return:
    '''
    ipa = '%s/student/student_info/%s/' % (settings.DOMAIN_NAME, nid)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=8
    )

    qr.add_data(ipa)
    qr.make(fit=True)
    img = qr.make_image()
    import uuid

    file_name = '%s.png' %(str(uuid.uuid4()))
    img.save('%s/school/Qrcode/%s' % (settings.MEDIA_ROOT, file_name))
    return file_name

