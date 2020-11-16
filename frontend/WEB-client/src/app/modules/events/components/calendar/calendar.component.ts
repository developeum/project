import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss']
})
export class CalendarComponent implements OnInit {
  numOfchosenDates: number = 0;
  checkDate: number;
  checkMonth: number;
  checkYear: number;
  minDate: string;
  minDateNum: number;
  maxDate: string;
  maxDateNum: number;

  fullDate = new Date();
  currMonth = this.fullDate.getMonth()+1;
  daysOfWeek = ["Пн","Вт","Ср","Чт","Пт","Сб","Вс"]
  dates: number[] = [];
  chosenMonth: number;
  lastMonthDates: number[] = [];
  bigMonth = [true, false, true, false, true, false , true, true ,false, true, false, true];
  months = [
    {
      name: 'Январь',
      id: 0
    },
    {
      name: 'Февраль',
      id: 1
    },
    {
      name: 'Март',
      id: 2
    },
    {
      name: 'Апрель',
      id: 3
    },
    {
      name: 'Май',
      id: 4
    },
    {
      name: 'Июнь',
      id: 5
    },
    {
      name: 'Июль',
      id: 6
    },
    {
      name: 'Август',
      id: 7
    },
    {
      name: 'Сентябрь',
      id: 8
    },
    {
      name: 'Октябрь',
      id: 9
    },
    {
      name: 'Ноябрь',
      id: 10
    },
    {
      name: 'Декабрь',
      id: 11
    },
  ]
  


  constructor() { }

  @Output() throwDate = new EventEmitter<string[]>()

  ngOnInit(): void {
    this.createCalendar()
  }

  createCalendar(){
    let date = new Date()
    let month = date.getMonth()
    let currentMonthParams = new Date(date.getFullYear(), month, 1)
    console.log(currentMonthParams);
    let dates = this.createDatesArray(currentMonthParams);
    this.lastMonthDates = dates.extraMonthDates;
    this.dates = dates.monthDates;
    this.chosenMonth = month
  }

  createMonth(newMonth: number){
    if( newMonth == 1){
      if(this.chosenMonth != 11){
        this.chosenMonth++;
        this.currMonth = this.chosenMonth+1;
        let newDate = new Date(this.fullDate.getFullYear(), this.chosenMonth, 1)
        let newDatesArr = this.createDatesArray(newDate);
        this.dates = newDatesArr.monthDates;
        this.lastMonthDates = newDatesArr.extraMonthDates;
        this.fullDate = newDate;
      } else {
        this.chosenMonth = 0;
        this.currMonth = 1;
        let newDate = new Date(this.fullDate.getFullYear()+1, this.chosenMonth, 1);
        let newDatesArr = this.createDatesArray(newDate);
        this.dates = newDatesArr.monthDates;
        this.lastMonthDates = newDatesArr.extraMonthDates;
        this.fullDate = newDate;
      }
    } else {
      if(this.chosenMonth != 0){
        this.chosenMonth--;
        this.currMonth = this.chosenMonth+1;
        let newDate = new Date(this.fullDate.getFullYear(), this.chosenMonth, 1)
        let newDatesArr = this.createDatesArray(newDate);
        this.dates = newDatesArr.monthDates;
        this.lastMonthDates = newDatesArr.extraMonthDates;
        this.fullDate = newDate;
      } else {
        this.chosenMonth = 11;
        this.currMonth = this.chosenMonth+1;
        let newDate = new Date(this.fullDate.getFullYear()-1, this.chosenMonth, 1);
        let newDatesArr = this.createDatesArray(newDate);
        this.dates = newDatesArr.monthDates;
        this.lastMonthDates = newDatesArr.extraMonthDates;
        this.fullDate = newDate;
      }
    }
  }

  nextMonth(){
    this.createMonth(1)
  }

  prevMonth(){
    this.createMonth(0)
  }

  setDate(currentDate){
    this.numOfchosenDates++
    if(this.numOfchosenDates == 3 ){
      this.numOfchosenDates = 1;
    }
    if((currentDate <= this.checkDate || (this.fullDate.getMonth() < this.checkMonth && this.fullDate.getFullYear() >= this.checkYear) || this.fullDate.getFullYear() < this.checkYear) && this.numOfchosenDates == 2){
      this.numOfchosenDates = 1;
    }
    switch(this.numOfchosenDates) {
      case 3: {
        this.numOfchosenDates = 1;
        this.maxDate = null;
        this.minDate = null;
      };
      case 1:{
        this.checkDate = currentDate;
        this.checkMonth = this.fullDate.getMonth();
        this.checkYear = this.fullDate.getFullYear();
        if(this.currMonth/10 < 1){
          if (currentDate/10 < 1){
            this.minDate = this.fullDate.getFullYear() + '-0' + this.currMonth + '-0' + currentDate;
            this.minDateNum = currentDate - 1
          } else {
            this.minDate = this.fullDate.getFullYear() + '-0' + this.currMonth + '-' + currentDate;
            this.minDateNum = currentDate - 1
          }
        } else {
          if (currentDate/10 < 1){
            this.minDate = this.fullDate.getFullYear() + '-' + this.currMonth + '-0' + currentDate;
            this.minDateNum = currentDate - 1
          } else {
            this.minDate = this.fullDate.getFullYear() + '-' + this.currMonth + '-' + currentDate;
            this.minDateNum = currentDate - 1
          }
        } 
      } 
      case 2:{
        if(this.currMonth/10 < 1){
          if (currentDate/10 < 1){
            this.maxDate = this.fullDate.getFullYear() + '-0' + this.currMonth + '-0' + currentDate;
            this.maxDateNum = currentDate - 1
          } else {
            this.maxDate = this.fullDate.getFullYear() + '-0' + this.currMonth + '-' + currentDate;
            this.maxDateNum = currentDate - 1
          }
        } else {
          if (currentDate/10 < 1){
            this.maxDate = this.fullDate.getFullYear() + '-' + this.currMonth + '-0' + currentDate;
            this.maxDateNum = currentDate - 1
          } else {
            this.maxDate = this.fullDate.getFullYear() + '-' + this.currMonth + '-' + currentDate;
            this.maxDateNum = currentDate - 1
          }
        }
      } 
    }
    let arrayForThrowing: string[] = []
    
    arrayForThrowing.push(this.minDate);
    arrayForThrowing.push(this.maxDate)
    this.throwDate.emit(arrayForThrowing);
  }

  createDatesArray(monthInfo: Date){
    let extraMonthDates = []
    let monthDates = [];
    let currDayOfWeek: number = monthInfo.getDay();
    if(this.bigMonth[monthInfo.getMonth()]){ //its big month
      console.log("big month")
      let maxDay = 30;
      if(monthInfo.getMonth() == 7 || monthInfo.getMonth() == 0){
        maxDay = 31
      }
      
      if(monthInfo.getDay() == 0){
        for(let day = 6; day > 0; day--){
          extraMonthDates.push(maxDay);
          maxDay--;
        }
      } else {
        for(let day = monthInfo.getDay(); day > 1; day--){
          extraMonthDates.push(maxDay);
          maxDay--;
        }
      }
      extraMonthDates.reverse()
      for (let day = 0; day < 31; day++){
        monthDates.push(day + 1)
      }


    } else { //its small month
      console.log("small month")
      let maxDay = 31;
      if(monthInfo.getDay() == 0){
        for(let day = 6; day > 0; day--){
          extraMonthDates.push(maxDay);
          maxDay--;
        }
      } else {
        for(let day = monthInfo.getDay(); day > 1; day--){
          extraMonthDates.push(maxDay);
          maxDay--;
        }
      }
      extraMonthDates.reverse();
      if(this.chosenMonth == 1){ //february
        if((this.fullDate.getFullYear() % 4) == 0){
          for(let day = 0; day < 29; day++){
            monthDates.push(day + 1)
          }
        } else {
          for( let day = 0; day < 28; day++){
            monthDates.push(day + 1)
          }
        }
        
      } else {
        for (let day = 0; day < 30; day++){//classic months
          monthDates.push(day + 1)
        }
      }
      

    }
    console.log(monthDates);
    return {extraMonthDates, monthDates};
  }
}
