import { HandlerToDeleteVM } from "./handler";

const handlerToRemoveVirtualMachine = new HandlerToDeleteVM('.container', '.close');
handlerToRemoveVirtualMachine.addEventListeners();