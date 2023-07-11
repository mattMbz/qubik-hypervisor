import { HandlerToDeleteVM, HandlerToSearching } from "./handler";

const handlerToSearching = new HandlerToSearching('#searcherInput');
const handlerToRemoveVirtualMachine = new HandlerToDeleteVM('.container', '.close');

handlerToRemoveVirtualMachine.addEventListeners();
handlerToSearching.addEventListenerForSearcherInput();