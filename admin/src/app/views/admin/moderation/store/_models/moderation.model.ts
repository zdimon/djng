/* -----  --- */
import { BaseModel } from '@core/_base/crud';


export class ModerationModel extends BaseModel {
    
        
            id: number;
        
    
        
    
        
            name: string;
        
    
        
            type_obj: string;
        
    

    clear() {
        
            
                
                
                    this.id = 0 ;
                
            
         
            
         
            
                
                    this.name = '' ;
                
                
            
         
            
                
                    this.type_obj = '' ;
                
                
            
         
    }
}
