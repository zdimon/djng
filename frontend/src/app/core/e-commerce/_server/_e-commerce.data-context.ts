import { CarSpecificationsTable } from './car-specifications.table';
import { CarsTable } from './cars.table';
import { CustomersTable } from './customers.table';
import { OrdersTable } from './orders.table';
import { RemarksTable } from './remarks.table';

// Wrapper class
export class ECommerceDataContext {
    public static customers: any = CustomersTable.customers;

    public static cars: any = CarsTable.cars;

    // e-commerce car remarks
    // one => many relations
    public static remarks = RemarksTable.remarks;

    // e-commerce car specifications
    // one => many relations
    public static carSpecs = CarSpecificationsTable.carSpecifications;

    public static orders = OrdersTable.orders;
}
