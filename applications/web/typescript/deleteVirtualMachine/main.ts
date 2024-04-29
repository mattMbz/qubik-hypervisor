import { HandlerToDeleteVM, HandlerToSearching } from "./handlers";

const handlerToSearching = new HandlerToSearching('#searcherInput');
const handlerToRemoveVirtualMachine = new HandlerToDeleteVM('.container', '.close');

handlerToRemoveVirtualMachine.addEventListeners();
handlerToSearching.addEventListenerForSearcherInput();