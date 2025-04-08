N = int(input())
arr = [0] * 10
num = 1
def make_nine(N):
    while N % 10 != 9:
        for i in str(N):
            arr[int(i)] += num
        N -= 1
    return N
# 1의 자릿수부터 num 만큼 증가시키며 연산한다.
# N을 10씩 나눠가며 현재 자릿수를 증가시킨다.
# 자릿수가 커질수록 num을 10씩 곱한다.
while N > 0:
    # N의 현재 마지막 자릿수를 9로 맞춰준다
    N = make_nine(N)
    if N < 10:
        for i in range(N + 1):
            arr[i] += num
    else:
        for i in range(10):
            arr[i] += (N // 10 + 1) * num
    arr[0] -= num
    num *= 10
    N //= 10
for i in range(0, 10):
    print(arr[i], end=' ')