from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import import_key
from Crypto.Util.number import long_to_bytes
from sage.all import *

def cubeRoot(cipher):
    cipher = Integer(cipher)
    cube_root = cipher.nth_root(3)
    return long_to_bytes(cube_root)

if __name__ == "__main__":

    c1 = 1117464713471520760092856742380650974968064801694731457782656283801166681255111613229507025810479334694764622123718451297570426853961716946754271720095672233961117978764386596746168336071055644546249044566070611864310090957180283149806294936134109519888294592978328186668031907589841013887313896156754836773871253011053202477093481737002036144132468269675140638318982284875161893121578080092092615094120670638753419595899658845188924684802740246548159759367459050969013
    pk11 = """-----BEGIN PUBLIC KEY-----
    MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAr2wJAVAOVwioH/TA7V3g
    WxKyUJYZHnKMfsP7yN4P1CHhbRdbfDx6oGMMXdq1jPHfSmXPl+skbfPe0hTrKV4S
    py91BDk25U4TeH5hEMZMOlcjg+ZlrSHAaur9OLlF3CA0VYxgA/Uhue+lf/l/jNOe
    Rnh1fgZLlYCVfEduVpSYYIAE7B6G88n6fdkyUxZOrB8e24n/NdsN3qCtslrRx8gq
    aTz9hv3ugblbLgowAX4hIaL7b3pZflyeyWiTU1hpCHsAPGHNRYJuwBmnbSNy3cKM
    4cfgU/PgMH+GwlzvPpdpQG1R2UTgMB+OlE0XZFHFmfIPOhgCo4Haa7qAWnv9gn9L
    UwIBAw==
    -----END PUBLIC KEY-----"""
    pk12 = """-----BEGIN PUBLIC KEY-----
    MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEA5llbvhjKK0nPm0IlarLy
    gPBlOc17SfHLR1rmiYRvVIW4WSz+xzyFhgUbsnneH+8+WQn+dZ9KuXZEefGw1G4K
    hVUn3PfWGzv66tOwyg77Pjy8Cvwf4RHaglXqYbNfzml6vmULE8akVhz0gZL7lKdt
    QdSSMd4QG4FmHIQ7+yeVA87bctJNzfQZiXn/e3lKgVMZIkZ3gxOS8hjN/0yCr1VN
    RoM7Jrp/KYBnZKFORRDlLGyFnvJj9EOCqMSGtHlnc+Iq9QKWfebHUnJytwy1DSQh
    R7/Db944S8u90ar7R7W+AIdv2RpRF86/f3VUUiHFVdUpONpGLnQOd0x1ciEVNKg3
    MwIBAw==
    -----END PUBLIC KEY-----"""
    pk13 = """-----BEGIN PUBLIC KEY-----
    MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEArBr5tQUCbVl7QNM4qjfY
    eIlOoC6l6yXqSIgKgwl2QAps0frUERwqFvsL3wBGmX0yIXqiNSveJDpKcGsXa56I
    BUD4CxHN+EJI4J90ShRl4e1w4OGkZjq7JaG57uS4VTJ23ndbzFWq/L3sPRO76q/A
    PWgG7V5iRZFk59otWn2gjdalg3WChwj7j4tu1WAspqnivCKKjbFf2VfWV1FItUMM
    YM17pIfJ5AyCpZdEnX4+y1OABtpLCh2INw9eKYJY1WaHOWOWxAhb31JuaPmMqfJp
    BU4AdfGEpsmYq4lAb2GstFFEuRZHP/G5j8XghQC4n9LzbjMNRzFryMWkpu3WUiCM
    nwIBAw==
    -----END PUBLIC KEY-----"""
    pk14 = """-----BEGIN PUBLIC KEY-----
    MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAm6pxBv4X2SkKd4o0tJ27
    acezuYwdpSLeFrayj3Nvhx1vPDySCZzIac1xlpgYVrcAcloeNfNqc7sFht7Gj/HS
    N+aWB3o5tHCGrbaPo+o6ZtyZeia8CSqGA7BT6txzjXbpxA4gSl5GNqzUHFYa/KNy
    7UFqqOMEZS2g1spbS09/CElhFnuxRjkjnUuB47glNhG19k+78cfouerrZSUECWcN
    gDD9sODyog3wyXUvQ8wo4ZTeqsAcRH1A6xLFJ61lxlWYSlxXs9oEq5rGg40wUSqW
    i8bSL4ubPhJto/j7NzlKMP4KTRqfSp5DCwqAjCt96BmVfgGTRfW3KM809UHUeAo0
    JwIBAw==
    -----END PUBLIC KEY-----"""
    c2 = 7158742334638786791867157399077026607781320234489466468544238467187963463614925982063472605441213054416525055698590683094831261230094219941895978935840763042539688580972704071433278586135223690173991036112551590986431756845598879927390026459351110577119171836797997176836000874883254250921737562958603963973662466277126680704930555572487093877848745265507711030291836649063629979937348616900073324056791162399189203743018642504394125905791699027766210152606983582526435017971572297451170252678320070925527727413731875114877502502342950873125519627557902185529929085470413798504760978197225630557078467208137178670159
    c3 = 11763430165672227162533425800678907121879005465156402789290549525950775594393094005744826658676483697081580456447209147905463275060170447775648131515211858730164619240941429192001706622989518174664198392274580493994886052251004604670980574124744462633183057000523323708886035155805826782392778618833195804704348363665798160157214097844046054214071452122961984934357632262521132018376423442424100105806153563702242523862081267519441541268554064518907758489489430064250150390000748562873449000782137174512548022990430370918251350681669069684057779916934320900859820646303776058615012620442750519920020399456527106874539
    c4 = 10091252333004207449667397843863914106792386769524914162610757946804861925223666194375048819153461816569278150340458207377755051978314389342263554786067258260799216732221458958146074975976620512018065514688413811106231718445996816872844810778218794144812754404511433917228201189295678487566247297916775442836203875915306424510977557805967649499691814593576440130930371266161785868932510577414220095484898712963073680908184765143814105157738300422118723758377319312152356948499169788563864411114734943201770767553099904689276596803050347659249426964890215189941372071678320815818340855594985265436611894766626318456481


    print("First message :", cubeRoot(c1))

    pk12 = RSA.importKey(pk12)
    pk13 = RSA.importKey(pk13)
    pk14 = RSA.importKey(pk14)

    x = crt([c2,c3,c4],[pk12.n,pk13.n,pk14.n])
    print("Second message (CRT) :", cubeRoot(x))

