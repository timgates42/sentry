import {projectStatsToSeries} from 'sentry/views/settings/project/server-side-sampling/utils/projectStatsToSeries';

describe('projectStatsToSeries', function () {
  it('returns correct series', function () {
    expect(projectStatsToSeries(TestStubs.Outcomes())).toEqual([
      {
        seriesName: 'Indexed and Processed',
        color: 'hsl(340.79999999999995, 61%, 79.4%)',
        barMinHeight: 1,
        type: 'bar',
        stack: 'usage',
        data: [
          {name: 1656788400000, value: 294117},
          {name: 1656792000000, value: 281850},
          {name: 1656795600000, value: 263003},
          {name: 1656799200000, value: 259581},
          {name: 1656802800000, value: 246831},
          {name: 1656806400000, value: 278464},
          {name: 1656810000000, value: 290677},
          {name: 1656813600000, value: 242770},
          {name: 1656817200000, value: 242559},
          {name: 1656820800000, value: 248963},
          {name: 1656824400000, value: 250920},
          {name: 1656828000000, value: 268994},
          {name: 1656831600000, value: 296129},
          {name: 1656835200000, value: 308165},
          {name: 1656838800000, value: 302398},
          {name: 1656842400000, value: 301891},
          {name: 1656846000000, value: 316698},
          {name: 1656849600000, value: 333888},
          {name: 1656853200000, value: 336204},
          {name: 1656856800000, value: 329735},
          {name: 1656860400000, value: 323717},
          {name: 1656864000000, value: 317564},
          {name: 1656867600000, value: 312407},
          {name: 1656871200000, value: 307008},
          {name: 1656874800000, value: 301681},
          {name: 1656878400000, value: 299652},
          {name: 1656882000000, value: 276849},
          {name: 1656885600000, value: 274486},
          {name: 1656889200000, value: 298985},
          {name: 1656892800000, value: 368148},
          {name: 1656896400000, value: 444434},
          {name: 1656900000000, value: 423119},
          {name: 1656903600000, value: 416110},
          {name: 1656907200000, value: 464443},
          {name: 1656910800000, value: 526387},
          {name: 1656914400000, value: 692300},
          {name: 1656918000000, value: 720026},
          {name: 1656921600000, value: 719854},
          {name: 1656925200000, value: 719658},
          {name: 1656928800000, value: 719237},
          {name: 1656932400000, value: 717889},
          {name: 1656936000000, value: 719757},
          {name: 1656939600000, value: 718147},
          {name: 1656943200000, value: 719843},
          {name: 1656946800000, value: 712099},
          {name: 1656950400000, value: 643028},
          {name: 1656954000000, value: 545065},
          {name: 1656957600000, value: 311310},
        ],
      },
      {
        seriesName: 'Processed',
        color: '#F55459',
        data: [
          {name: 1656788400000, value: 250},
          {name: 1656792000000, value: 279},
          {name: 1656795600000, value: 249},
          {name: 1656799200000, value: 251},
          {name: 1656802800000, value: 463},
          {name: 1656806400000, value: 270},
          {name: 1656810000000, value: 285},
          {name: 1656813600000, value: 256},
          {name: 1656817200000, value: 633},
          {name: 1656820800000, value: 267},
          {name: 1656824400000, value: 326},
          {name: 1656828000000, value: 335},
          {name: 1656831600000, value: 258},
          {name: 1656835200000, value: 255},
          {name: 1656838800000, value: 614},
          {name: 1656842400000, value: 293},
          {name: 1656846000000, value: 717},
          {name: 1656849600000, value: 523},
          {name: 1656853200000, value: 311},
          {name: 1656856800000, value: 287},
          {name: 1656860400000, value: 294},
          {name: 1656864000000, value: 1398},
          {name: 1656867600000, value: 260},
          {name: 1656871200000, value: 292},
          {name: 1656874800000, value: 242},
          {name: 1656878400000, value: 318},
          {name: 1656882000000, value: 326},
          {name: 1656885600000, value: 302},
          {name: 1656889200000, value: 300},
          {name: 1656892800000, value: 301},
          {name: 1656896400000, value: 321},
          {name: 1656900000000, value: 310},
          {name: 1656903600000, value: 320},
          {name: 1656907200000, value: 373},
          {name: 1656910800000, value: 980},
          {name: 1656914400000, value: 45913},
          {name: 1656918000000, value: 143992},
          {name: 1656921600000, value: 168335},
          {name: 1656925200000, value: 168420},
          {name: 1656928800000, value: 128072},
          {name: 1656932400000, value: 114930},
          {name: 1656936000000, value: 148618},
          {name: 1656939600000, value: 163206},
          {name: 1656943200000, value: 153355},
          {name: 1656946800000, value: 81371},
          {name: 1656950400000, value: 17657},
          {name: 1656954000000, value: 903},
          {name: 1656957600000, value: 1250},
        ],
        barMinHeight: 1,
        type: 'bar',
        stack: 'usage',
      },
      {
        seriesName: 'Dropped',
        color: '#F5B000',
        data: [
          {name: 1656788400000, value: 0},
          {name: 1656792000000, value: 1},
          {name: 1656795600000, value: 1},
          {name: 1656799200000, value: 1},
          {name: 1656802800000, value: 94},
          {name: 1656806400000, value: 1},
          {name: 1656810000000, value: 1},
          {name: 1656813600000, value: 0},
          {name: 1656817200000, value: 566},
          {name: 1656820800000, value: 179},
          {name: 1656824400000, value: 1},
          {name: 1656828000000, value: 1},
          {name: 1656831600000, value: 1},
          {name: 1656835200000, value: 0},
          {name: 1656838800000, value: 222},
          {name: 1656842400000, value: 6},
          {name: 1656846000000, value: 287},
          {name: 1656849600000, value: 465},
          {name: 1656853200000, value: 83},
          {name: 1656856800000, value: 7},
          {name: 1656860400000, value: 0},
          {name: 1656864000000, value: 1835},
          {name: 1656867600000, value: 145},
          {name: 1656871200000, value: 0},
          {name: 1656874800000, value: 0},
          {name: 1656878400000, value: 1},
          {name: 1656882000000, value: 0},
          {name: 1656885600000, value: 0},
          {name: 1656889200000, value: 0},
          {name: 1656892800000, value: 1},
          {name: 1656896400000, value: 0},
          {name: 1656900000000, value: 2},
          {name: 1656903600000, value: 0},
          {name: 1656907200000, value: 1},
          {name: 1656910800000, value: 849},
          {name: 1656914400000, value: 25331},
          {name: 1656918000000, value: 147200},
          {name: 1656921600000, value: 220014},
          {name: 1656925200000, value: 189001},
          {name: 1656928800000, value: 99590},
          {name: 1656932400000, value: 81288},
          {name: 1656936000000, value: 134522},
          {name: 1656939600000, value: 151489},
          {name: 1656943200000, value: 128585},
          {name: 1656946800000, value: 41643},
          {name: 1656950400000, value: 6404},
          {name: 1656954000000, value: 145},
          {name: 1656957600000, value: 1381},
        ],
        barMinHeight: 1,
        type: 'bar',
        stack: 'usage',
      },
    ]);
  });
});
