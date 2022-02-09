/* -----  --- */
import { BaseModel } from '@core/_base/crud';


export class PaymentTypeModel extends BaseModel {
    
        
            id: number;
        
    
        
            name: string;
        
    
        
            procent_for_agency: number;
        
    
        
            alias: string;
        
    
        
            price: number;
        
    

    clear() {
        
            
                
                
                    this.id = 0 ;
                
            
         
            
                
                    this.name = '' ;
                
                
            
         
            
                
                
                    this.procent_for_agency = 0 ;
                
            
         
            
                
                    this.alias = '' ;
                
                
            
         
            
                
                
                    this.price = 0 ;
                
            
         
    }
}
