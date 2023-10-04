-- Crea la tabla de usuarios
create table CreditCard (
  numero text not null,
  cedula varchar( 20 )  NOT NULL,
  nombre text not null,
  banco text not null,
  fecha_de_vencimiento varchar(20),
  franquicia text,
  pago_mes text not null,
  cuota_manejo text not null,
  tasa_interes text NOT NULL
); 

create table Amortizaciones (
  cedula_usuario text not null,
  payment text not null,
  interest varchar( 20 )  NOT NULL,
  amortizacion text not null,
  balance text not null
  pay_date date not null
);