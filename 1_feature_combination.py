from request.login import testLoginSuccess, testLoginInvalidUserOrPass, testLoginInvalidBody
from request.refresh import testRefreshSuccess, testRefreshInvalid, testRefreshProtected, testRefreshReuse, testRefreshInvalidBody

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
        testRefreshInvalidBody()
        
testFeatureCombination(True, True)
testFeatureCombination(True, False)