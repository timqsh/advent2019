Перем Указатель;
Перем Вывод;
Перем Ввод;
Перем Память;

Процедура Сделать()
	
	Память = СтрРазделить(ПамятьСтрока, ",");
	Для К = 0 По Память.Количество() - 1 Цикл
		Память[К] = Число(Память[К]);
	КонецЦикла;
	Ввод = Число(ВводСтрока);
	
	Указатель = 0;
	Вывод = Новый Массив;
	Пока Истина Цикл
		КодПараметры = Память[Указатель];
		Указатель = Указатель + 1;
		
		Код = КодПараметры % 100;
		ПараметрыЧислом = Цел(КодПараметры / 100);
		
		Если Код = 99 Тогда
			Прервать;
		КонецЕсли;
		
		Результат = ИмяФункцииЧислоАргументов(Код);
		ИмяФункции = Результат[0];
		ЧислоАргументов = Результат[1];
		
		Аргументы = "";
		Для К = 0 По ЧислоАргументов - 1 Цикл
			Позиционно = (ПараметрыЧислом % 10) = 0;
			ПараметрыЧислом = Цел(ПараметрыЧислом / 10);
			
			Аргумент = Формат(Память[Указатель], "ЧГ=;ЧН=0"); // 9 000 -> "9000"
			Указатель = Указатель + 1;
			
			Если Позиционно Тогда
				Аргументы = Аргументы + "Память[" + Аргумент + "],";
			Иначе
				Аргументы = Аргументы + Аргумент + ",";
			КонецЕсли
		КонецЦикла;
		Аргументы = Лев(Аргументы, СтрДлина(Аргументы) - 1); // убрать "," в конце
		
		Выполнить(ИмяФункции + "(" + Аргументы + ")");
	КонецЦикла;
	
	Сообщить(СтрСоединить(Вывод, ","));
	
КонецПроцедуры

Функция ИмяФункцииЧислоАргументов(Код)
	
	Если      Код = 1 Тогда Возврат СложитьВМассив("Сложить", 3);
	ИначеЕсли Код = 2 Тогда Возврат СложитьВМассив("Умножить", 3);
	ИначеЕсли Код = 3 Тогда Возврат СложитьВМассив("Ввод", 1);
	ИначеЕсли Код = 4 Тогда Возврат СложитьВМассив("Вывод", 1);
	ИначеЕсли Код = 5 Тогда Возврат СложитьВМассив("ПерейтиИстина", 2);
	ИначеЕсли Код = 6 Тогда Возврат СложитьВМассив("ПерейтиЛожь", 2);
	ИначеЕсли Код = 7 Тогда Возврат СложитьВМассив("Меньше", 3);
	ИначеЕсли Код = 8 Тогда Возврат СложитьВМассив("Равно", 3);
	КонецЕсли;
	
КонецФункции

Функция СложитьВМассив(Парам1, Парам2)
	
	Результат = Новый Массив();
	Результат.Добавить(Парам1);
	Результат.Добавить(Парам2);
	Возврат Результат;
	
КонецФункции

Функция Сложить(а, б, Результат)
	
	Результат = а + б;
	
КонецФункции

Функция Умножить(а, б, Результат)
	
	Результат = а * б;
	
КонецФункции

Функция Ввод(Значение)
	
	Значение = Ввод;
	
КонецФункции

Функция Вывод(Значение)
	
	Вывод.Добавить(Значение);
	
КонецФункции

Функция ПерейтиИстина(Условие, Адрес)
	
	Если Условие <> 0 Тогда
		Указатель = Адрес;
	КонецЕсли
	
КонецФункции

Функция ПерейтиЛожь(Условие, Адрес)
	
	Если Условие = 0 Тогда
		Указатель = Адрес;
	КонецЕсли
	
КонецФункции

Функция Меньше(а, б, Результат)
	
	Результат = ?(а < б, 1, 0);
	
КонецФункции

Функция Равно(а, б, Результат)
	
	Результат = ?(а = б, 1, 0);
	
КонецФункции
