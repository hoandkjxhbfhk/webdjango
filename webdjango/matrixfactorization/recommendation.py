import numpy as np
import pandas as pd
import scipy.optimize
from shop.models import Review


def Myrecommend():
    def normalizeRatings(myY, myR):
        # The mean is only counting movies that were rated
        Ymean = np.sum(myY, axis=1) / np.sum(myR, axis=1)
        Ymean = Ymean.reshape((Ymean.shape[0], 1))
        return myY - Ymean, Ymean

    def flattenParams(myX, myTheta):
        return np.concatenate((myX.flatten(), myTheta.flatten()))

    def reshapeParams(flattened_XandTheta, mynm, mynu, mynf):
        assert flattened_XandTheta.shape[0] == int(mynm * mynf + mynu * mynf)
        reX = flattened_XandTheta[: int(mynm * mynf)].reshape((mynm, mynf))
        reTheta = flattened_XandTheta[int(mynm * mynf) :].reshape((mynu, mynf))
        return reX, reTheta

    def cofiCostFunc(myparams, myY, myR, mynu, mynm, mynf, mylambda=0.0):
        myX, myTheta = reshapeParams(myparams, mynm, mynu, mynf)
        term1 = myX.dot(myTheta.T)
        term1 = np.multiply(term1, myR)
        cost = 0.5 * np.sum(np.square(term1 - myY))
        # for regularization
        cost += (mylambda / 2.0) * np.sum(np.square(myTheta))
        cost += (mylambda / 2.0) * np.sum(np.square(myX))
        return cost

    def cofiGrad(myparams, myY, myR, mynu, mynm, mynf, mylambda=0.0):
        myX, myTheta = reshapeParams(myparams, mynm, mynu, mynf)
        term1 = myX.dot(myTheta.T)
        term1 = np.multiply(term1, myR)
        term1 -= myY
        Xgrad = term1.dot(myTheta)
        Thetagrad = term1.T.dot(myX)
        # Adding Regularization
        Xgrad += mylambda * myX
        Thetagrad += mylambda * myTheta
        return flattenParams(Xgrad, Thetagrad)

    df = pd.DataFrame(list(Review.objects.all().values()))
    print(df)
    # mynu = df.user_id.unique().shape[0]
    mynu = df.user_name.unique().shape[0]
    # mynm = df.movie_id.unique().shape[0]
    mynm = df.product_id.unique().shape[0]
    mynf = 10
    Y = np.zeros((mynm, mynu))

    user_to_column = {}  # Tạo một bản đồ từ tên người dùng sang chỉ số cột
    # Duyệt qua tất cả các người dùng trong dataframe và gán mỗi tên người dùng với một chỉ số cột
    for idx, user_name in enumerate(df["user_name"].unique()):
        user_to_column[user_name] = idx

    product_to_row = {}  # Tạo một bản đồ từ product_id sang chỉ số hàng
    # Duyệt qua tất cả các product_id trong dataframe và gán mỗi product_id với một chỉ số hàng
    for idx, product_id in enumerate(df["product_id"].unique()):
        product_to_row[product_id] = idx
    for row in df.itertuples():
        # Y[row[2] - 1, row[4] - 1] = row[3]
        # if row[1] not in product_to_row or row[4] not in user_to_column.values():
        #     print(row[1],row[4])
        #     continue  # Bỏ qua các dòng không thể ánh xạ
        Y[product_to_row[row[2]], user_to_column[row[4]]] = row[6]

    print(user_to_column)
    print(product_to_row)
    print(Y)
    R = np.zeros((mynm, mynu))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            if Y[i][j] != 0:
                R[i][j] = 1

    print(R)
    Ynorm, Ymean = normalizeRatings(Y, R)
    X = np.random.rand(mynm, mynf)
    Theta = np.random.rand(mynu, mynf)
    myflat = flattenParams(X, Theta)

    # mylambda = 12.2
    # result = scipy.optimize.fmin_cg(cofiCostFunc, x0=myflat, fprime=cofiGrad, args=(Y, R, mynu, mynm, mynf, mylambda),
    #                                 maxiter=40, disp=True, full_output=True)
    # resX, resTheta = reshapeParams(result[0], mynm, mynu, mynf)
    # prediction_matrix = resX.dot(resTheta.T)
    # print(prediction_matrix)
    # return prediction_matrix, Ymean ,product_to_row ,user_to_column
    result = scipy.optimize.minimize(
        fun=cofiCostFunc,
        x0=myflat,
        args=(Ynorm, R, mynu, mynm, mynf, 0),
        method="TNC",
        jac=cofiGrad,
        options={"maxiter": 100},
    )

    resX, resTheta = reshapeParams(result.x, mynm, mynu, mynf)
    prediction_matrix = resX.dot(resTheta.T)
    print(prediction_matrix)
    return prediction_matrix, Ymean, product_to_row, user_to_column
