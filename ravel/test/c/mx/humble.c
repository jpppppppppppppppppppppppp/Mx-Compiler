#include <stdio.h>
#include <stdlib.h>

// USACO 3.1.3 humble
int MAXK = 105;
int MAXN = 100005;

int main() {
  int point = 0;
  int k;
  int MIN;
  int K;
  int N;
  int i;
  int *primes = malloc(sizeof(int) * MAXK);
  int *pindex = malloc(sizeof(int) * MAXK);
  int *ans = malloc(sizeof(int) * MAXN);
  scanf("%d%d", &K, &N);
  for (i = 0; i < K; ++i) {
    scanf("%d", &primes[i]);
    pindex[i] = 0;
  }
  ans[0] = 1;
  while (point <= N) {
    MIN = 2139062143;
    for (i = 0; i < K; ++i) {
      while (ans[point] >= primes[i] * ans[pindex[i]])
        pindex[i]++;
      if (primes[i] * ans[pindex[i]] < MIN) {
        MIN = primes[i] * ans[pindex[i]];
        k = i;
      }
    }
    ans[++point] = MIN;
  }
  printf("%d\n", ans[N]);
  return 0;
}

/*!! metadata:
=== comment ===
humble-5140519064-yurongyou.txt
=== is_public ===
True
=== assert ===
output
=== timeout ===
1.0
=== input ===
100 100000
2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97 101 103
107 109 113 127 131 137 139 149 151 157 163 167 173 179 181 191 193 197 199 211
223 227 229 233 239 241 251 257 263 269 271 277 281 283 293 307 311 313 317 331
337 347 349 353 359 367 373 379 383 389 397 401 409 419 421 431 433 439 443 449
457 461 463 467 479 487 491 499 503 509 521 523 541
=== phase ===
codegen extended
=== output ===
284456
=== exitcode ===


!!*/
