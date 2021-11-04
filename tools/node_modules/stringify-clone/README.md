# Stringify Clone [![version][npm-version]][npm-url] [![License][npm-license]][license-url]

Wrapper for fast object cloning using `JSON.parse` & `JSON.stringify`. see [Benchmarks](https://github.com/ahmadnassri/node-clone-benchmark).

**Notes**:

- cannot clone `RegExp` *(returns `{}`)*
- `NaN` values will be converted to `null`
- `Date` objects will be converted to ISO strings (equivalent of running `Date.toISOString()`)
  - you can reconstruct the Date by calling `new Date(string)`

[![Build Status][travis-image]][travis-url]
[![Downloads][npm-downloads]][npm-url]
[![Code Climate][codeclimate-quality]][codeclimate-url]
[![Coverage Status][codeclimate-coverage]][codeclimate-url]
[![Dependencies][david-image]][david-url]

## Install

```sh
npm install --save stringify-clone
```

## API

### clone()

```js
var clone = require('stringify-clone')

clone({
  foo: 'bar'
})
```

## Support

Donations are welcome to help support the continuous development of this project.

[![Gratipay][gratipay-image]][gratipay-url]
[![PayPal][paypal-image]][paypal-url]
[![Flattr][flattr-image]][flattr-url]
[![Bitcoin][bitcoin-image]][bitcoin-url]

## License

[MIT](LICENSE) &copy; [Ahmad Nassri](https://www.ahmadnassri.com)

[license-url]: https://github.com/ahmadnassri/stringify-clone/blob/master/LICENSE

[travis-url]: https://travis-ci.org/ahmadnassri/stringify-clone
[travis-image]: https://img.shields.io/travis/ahmadnassri/stringify-clone.svg?style=flat-square

[npm-url]: https://www.npmjs.com/package/stringify-clone
[npm-license]: https://img.shields.io/npm/l/stringify-clone.svg?style=flat-square
[npm-version]: https://img.shields.io/npm/v/stringify-clone.svg?style=flat-square
[npm-downloads]: https://img.shields.io/npm/dm/stringify-clone.svg?style=flat-square

[codeclimate-url]: https://codeclimate.com/github/ahmadnassri/stringify-clone
[codeclimate-quality]: https://img.shields.io/codeclimate/github/ahmadnassri/stringify-clone.svg?style=flat-square
[codeclimate-coverage]: https://img.shields.io/codeclimate/coverage/github/ahmadnassri/stringify-clone.svg?style=flat-square

[david-url]: https://david-dm.org/ahmadnassri/stringify-clone
[david-image]: https://img.shields.io/david/ahmadnassri/stringify-clone.svg?style=flat-square

[gratipay-url]: https://www.gratipay.com/ahmadnassri/
[gratipay-image]: https://img.shields.io/gratipay/ahmadnassri.svg?style=flat-square

[paypal-url]: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=UJ2B2BTK9VLRS&on0=project&os0=stringify-clone
[paypal-image]: http://img.shields.io/badge/paypal-donate-green.svg?style=flat-square

[flattr-url]: https://flattr.com/submit/auto?user_id=ahmadnassri&url=https://github.com/ahmadnassri/stringify-clone&title=stringify-clone&language=&tags=github&category=software
[flattr-image]: http://img.shields.io/badge/flattr-donate-green.svg?style=flat-square

[bitcoin-image]: http://img.shields.io/badge/bitcoin-1Nb46sZRVG3or7pNaDjthcGJpWhvoPpCxy-green.svg?style=flat-square
[bitcoin-url]: https://www.coinbase.com/checkouts/ae383ae6bb931a2fa5ad11cec115191e?name=stringify-clone
