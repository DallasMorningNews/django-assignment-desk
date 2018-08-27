import moment from 'moment';

const initializeMoment = () => {
  moment.defineLocale('en-us-apstyle', {
    meridiem(hour, minute, isLowercase) {
      let meridiemString;

      if (hour < 12) {
        meridiemString = 'a.m.';
      } else {
        meridiemString = 'p.m.';
      }

      if (!isLowercase) {
        return meridiemString.toUpperCase();
      }

      return meridiemString;
    },
    monthsShort: [
      'Jan.', 'Feb.', 'March', 'April', 'May', 'June',
      'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.',
    ],
    week: {
      dow: 0
    },
  });

  moment.locale('en-us-apstyle');

  return moment;
};

export default initializeMoment;
