from request.login import testLoginSuccess, testLoginInvalidUserOrPass, testLoginInvalidBody
from request.refresh import testRefreshSuccess, testRefreshInvalid, testRefreshProtected, testRefreshReuse

def testFeatureCombination(featureLogin: bool, featureRefresh: bool):
    if featureLogin:
        testLoginSuccess()
        testLoginInvalidUserOrPass()
        testLoginInvalidBody()
    if featureRefresh:
        testRefreshSuccess()
        testRefreshInvalid()
        testRefreshProtected()
        testRefreshReuse()
        
testFeatureCombination(True, True)