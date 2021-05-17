# Building Package

1. Check the version in the [VERSION](./VERSION) file.

1. Check the [CHANGELOG](./CHANGELOG.md).

1. (If anything is out of order, create a PR and merge updates to those.)

1. Execute the following push from master

```
git push origin master:release
```

CI should take it from there...


### Testing Deploy

During development, you can use a trailing version number, such as `0.1.1devXXX`. Push to the `test-release` branch to publish to a test PyPi. 