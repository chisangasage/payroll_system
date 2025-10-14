-- sample_data.sql
SET FOREIGN_KEY_CHECKS=0;
TRUNCATE TABLE payroll_payslip;
TRUNCATE TABLE payroll_payrollrun;
TRUNCATE TABLE payroll_employeeallowance;
TRUNCATE TABLE payroll_employeededuction;
TRUNCATE TABLE payroll_allowance;
TRUNCATE TABLE payroll_deduction;
TRUNCATE TABLE payroll_employee;
TRUNCATE TABLE payroll_department;
SET FOREIGN_KEY_CHECKS=1;

INSERT INTO payroll_department (id, name) VALUES (1,'HR'),(2,'IT'),(3,'Finance'),(4,'Sales');
INSERT INTO payroll_employee (id, first_name, last_name, employee_id, department_id, position, basic_salary, date_hired, gender) VALUES
  (1,'Alice','Mwansa','EMP001',2,'Developer',8000.00,'2022-03-15','F'),
  (2,'Joseph','Phiri','EMP002',3,'Accountant',6000.00,'2021-06-01','M'),
  (3,'Grace','Zimba','EMP003',1,'HR Officer',4500.00,'2023-01-10','F'),
  (4,'Brian','Kunda','EMP004',4,'Sales Rep',5200.00,'2020-09-20','M');
INSERT INTO payroll_allowance (id, name, amount) VALUES (1,'Transport',300.00),(2,'Housing',600.00),(3,'Performance Bonus',500.00);
INSERT INTO payroll_deduction (id, name, amount) VALUES (1,'Loan Repayment',200.00),(2,'Tax Advance',150.00);
INSERT INTO payroll_employeeallowance (id, employee_id, name, amount) VALUES (1,1,'Transport',300.00),(2,1,'Performance Bonus',500.00),(3,2,'Housing',600.00),(4,4,'Transport',300.00);
INSERT INTO payroll_employeededuction (id, employee_id, name, amount) VALUES (1,2,'Loan Repayment',200.00),(2,3,'Loan Repayment',150.00),(3,4,'Tax Advance',150.00);
INSERT INTO payroll_payrollrun (id, month, created_at, processed_by_id) VALUES (1,'2025-10-10',NOW(),NULL);
INSERT INTO payroll_payslip (id, payroll_id, employee_id, gross_pay, total_deductions, net_pay, created_at) VALUES
  (1,1,1,8800.00,1255.00,7545.00,NOW()),
  (2,1,2,6600.00,615.00,5985.00,NOW()),
  (3,1,3,4500.00,225.00,4275.00,NOW()),
  (4,1,4,5500.00,425.00,5075.00,NOW());
