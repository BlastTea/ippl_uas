from request.login import testLoginSuccess, testLoginInvalidUserAndPass, testLoginInvalidUser, testLoginInvalidPass, testLoginInvalidBody
from request.refresh import testRefreshSuccess, testRefreshInvalid, testRefreshProtected, testRefreshReuse, testRefreshInvalidBody

def testFeatureCombination(featureLogin: bool, featureRefresh: bool):
    if featureLogin:
        testLoginSuccess()
        testLoginInvalidUserAndPass()
        testLoginInvalidUser()
        testLoginInvalidPass()
        testLoginInvalidBody()
    if featureRefresh:
        testRefreshSuccess()
        testRefreshInvalid()
        testRefreshProtected()
        testRefreshReuse()
        testRefreshInvalidBody()
        
testFeatureCombination(True, True)