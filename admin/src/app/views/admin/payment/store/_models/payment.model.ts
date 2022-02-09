/* -----  --- */
import { BaseModel } from '@core/_base/crud';


export class PaymentModel extends BaseModel {
    
        
            id: number;
        
    
        
            ammount: number;
        
    

    clear() {
        
            
                
                
                    this.id = 0 ;
                
            
         
            
                
                
                    this.ammount = 0 ;
                
            
         
    }
}
